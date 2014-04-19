from __future__ import absolute_import
import time
import dateutil
import datetime
import eventlet
import logging
from django.conf import settings
try:
    from cPickle import load
except:
    from pickle import load

from dropbox import rest
from . import models

logger = logging.getLogger(__name__)

class Syncer(object):
    def __init__(self, client=None, force=True, threads=1):
        self.logger = logger.getChild(self.__class__.__name__)
        if not client:
            client = get_client()

        self.client = client
        self.force = force
        self.pool = eventlet.GreenPool(threads)
        self.queue = eventlet.Queue()

    def start(self, path=None):
        self.queue.put(dict(path=path or settings.DROPBOX_BASE_PATH))

        count = 0
        while True:
            while not self.queue.empty():
                count += 1
                self.pool.spawn_n(self.sync_file, **self.queue.get())

                self.logger.info(
                    'Processed %r files, %r currently running with %r waiting',
                    count,
                    self.pool.running(),
                    self.queue.qsize(),
                )
            self.pool.waitall()
            if self.queue.empty():
                break


    def sync_file(self, path, metadata=None, file_=None, parent=None):
        if metadata and metadata.is_dir:
            path = metadata.path +'/'

        if file_:
            self.logger.info('Updating path %r', path)
        else:
            try:
                file_ = (
                    models.File.objects.filter(path__iexact=path)
                    | models.File.objects.filter(path__iexact=path + '/')
                ).get()
                self.logger.info('Updating path %r', path)
            except models.File.DoesNotExist:
                self.logger.info('Found new path %r', path)
                file_ = models.File(
                    path=path,
                )

        if self.force:
            hash_ = None
            rev = None
        elif file_.is_directory:
            hash_ = file_.hash
            rev = None
        else:
            hash_ = None
            rev = file_.hash

        try:
            metadata = self.get_metadata(metadata, path, hash_, rev)

            if metadata.is_dir:
                file_.is_directory = True
            else:
                file_.is_file = True

            file_.hash = metadata.get('hash', metadata.get('rev'))
            file_.size = metadata.bytes
            file_.source = models.File.Source.dropbox
            file_.updated_at = metadata.modified

            if metadata.get('is_deleted'):
                file_.deleted_at = metadata.modified
            else:
                file_.deleted_at = None

            if metadata.get('contents'):
                file_.created_at = min(
                    f.modified for f in metadata['contents'])
            else:
                file_.created_at = datetime.datetime(
                    1970, 1, 1, tzinfo=dateutil.tz.tzutc())

            if parent:
                file_.parent = parent
            else:
                file_.parent = None

            file_.save()

            if file_.is_file:
                self.sync_revisions(file_)

            for child in metadata.get('contents', []):
                self.queue.put(dict(
                    path=child.path,
                    metadata=child,
                    parent=file_,
                ))

        except rest.ErrorResponse, e:
            self.logger.debug('No change in metadata for %r: %r', path,
                              file_.hash)
            if e.status != 304:
                raise
            else:
                for child in file_.children.directories():
                    self.pool.spawn_n(
                        self.sync_file, child.path, file_=child, parent=file_)

    def get_metadata(self, metadata, path, hash_, rev, retry=5):
        if metadata:
            if metadata.get('contents'):
                return metadata
            elif not metadata.is_dir:
                return metadata

        try:
            metadata = self.client.metadata(
                path,
                file_limit=25000,
                list=True,
                hash=hash_,
                rev=rev,
                include_deleted=True,
            )
        except rest.ErrorResponse, e:
            if e.status == 304:
                raise

            if not retry:
                self.logger.exception(
                    'Unable to fetch metadata for %r, %r, %r',
                    path, hash_, rev)
                raise

            time.sleep(1)
            return self.get_metadata(metadata, path, hash_, rev)

        self.logger.debug('Got updated metadata %r', metadata)
        return metadata

    def sync_revisions(self, file_):
        existing_revisions = dict((r.hash, r) for r in file_.revisions.all())
        oldest_revision = None
        for revision in self.client.revisions(path=file_.path, rev_limit=1000):
            if not oldest_revision or revision.modified < oldest_revision:
                oldest_revision = revision.modified

            if revision.rev not in existing_revisions:
                revision_object = models.Revision.objects.create(
                    file=file_,
                    path=revision.path,
                    hash=revision.rev,
                    deleted=revision.get('is_deleted', False),
                    created_at=revision.modified,
                )
                existing_revisions[revision.rev] = revision_object

        if oldest_revision:
            file_.created_at = oldest_revision
        else:
            file_.created_at = file_.modified
        file_.save()


def get_client():
    with open(settings.DROPBOX_SESSION_FILE, 'rb') as fh:
        sess = load(fh)

    from dropbox.client import DropboxClient
    return DropboxClient(sess)

