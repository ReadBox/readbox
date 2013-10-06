import os
from django.db import models
from django_utils import base_models, choices
from django.conf import settings
import denorm


class TagType(base_models.SlugMixin, base_models.CreatedAtModelBase):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    description = models.TextField(blank=True, null=True)
    color = models.IntegerField(blank=True, null=True)

    def tags_dict(self):
        tags = dict()
        for tag in self.tags.all():
            tags[tag.name] = tag
            tags[tag.name.lower()] = tag
        return tags

    class Meta(base_models.SlugMixin.Meta):
        pass


class Tag(base_models.NameMixin, base_models.CreatedAtModelBase):
    name = models.CharField(max_length=64)
    type = models.ForeignKey(TagType, related_name='tags')

    @classmethod
    def as_dict(self):
        tags = dict()
        for tag in self.objects.all():
            tags[tag.name] = tag
            tags[tag.name.lower()] = tag
        return tags

    class Meta:
        unique_together = 'name', 'type'


class Revision(base_models.NameMixin, base_models.ModelBase):
    file = models.ForeignKey('File', related_name='revisions')
    path = models.CharField(max_length=1024)
    hash = models.CharField(max_length=256)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    @property
    def name(self):
        return os.path.split(self.path.rstrip('/'))[-1]

    class Meta:
        unique_together = 'path', 'hash'


class FileManager(models.Manager):
    use_for_related_fields = True

    def all_directories(self):
        return self.get_query_set().filter(
            type=File.Type.directory,
        )

    def all_files(self):
        return self.get_query_set().filter(
            type=File.Type.file,
        )

    def directories(self):
        return self.visible().filter(
            type=File.Type.directory,
        )

    def files(self):
        return self.visible().filter(
            type=File.Type.file,
        )

    def visible(self):
        return self.get_query_set().filter(
            deleted_at__isnull=True,
        )


class FilePattern(base_models.NameMixin, base_models.CreatedAtModelBase):
    name = models.CharField(max_length=100)
    patterns = models.ManyToManyField('Pattern')

    class Meta:
        unique_together = 'name',


class Pattern(base_models.NameMixin, base_models.CreatedAtModelBase):
    name = models.CharField(max_length=100)
    pattern = models.CharField(max_length=250)
    example = models.TextField(blank=True, null=True)
    child_pattern = models.ForeignKey(FilePattern, blank=True, null=True)

    class Meta:
        unique_together = 'name',


class File(base_models.NameMixin, base_models.ModelBase):
    class Type(choices.Choices):
        block = choices.Choice('b', label='Block special file.')
        character = choices.Choice('c', label='Character special file.')
        directory = choices.Choice('d', label='Directory.')
        link = choices.Choice('l', label='Symbolic link.')
        socket = choices.Choice('s', label='Socket link.')
        pipe = choices.Choice('p', label='FIFO.')
        file = choices.Choice('-', label='Regular file.')

    class Source(choices.Choices):
        dropbox = choices.Choice()

    parent = models.ForeignKey(
        'File', blank=True, null=True, related_name='children')
    path = models.CharField(max_length=1024)
    name = models.CharField(max_length=256)
    hash = models.CharField(max_length=256)
    size = models.IntegerField()
    type = models.CharField(max_length=1, choices=Type.choices)
    source = models.IntegerField(
        choices=Source.choices,
        default=Source.dropbox,
    )
    tags = models.ManyToManyField(Tag, related_name='files')
    pattern = models.ForeignKey(FilePattern, null=True, blank=True)
    child_count = denorm.CountField('children')

    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = FileManager()

    def all_children(self):
        return File.objects.visible().filter(
            path__istartswith=self.path,
        ).exclude(pk=self.pk)

    def all_directories(self):
        return self.all_children().filter(type=File.Type.directory)

    def all_files(self):
        return self.all_children().filter(type=File.Type.file)

    def path_parts(self):
        base_path = settings.DROPBOX_BASE_PATH
        path_parts = self.path.split('/')
        for i in range(1, len(path_parts)):
            path = '/%s/' % os.path.join(*path_parts[:i])
            if path.startswith(base_path):
                yield path, path_parts[i - 1], path == base_path

    @property
    def extension(self):
        return os.path.splitext(self.name)[-1][1:]

    def get_log(self):
        assert self.source == File.Source.dropbox
        from . import dropbox
        client = dropbox.get_client()
        return client.revisions(self.path)

    def get_link(self):
        assert self.source == File.Source.dropbox
        from . import dropbox
        client = dropbox.get_client()
        return client.media(self.path).url

    def _get_is_directory(self):
        return self.type == File.Type.directory

    def _set_is_directory(self, value):
        assert value, 'Cannot disable `is_directory` without another value'
        self.type = File.Type.directory

    is_directory = property(_get_is_directory, _set_is_directory)

    def _get_is_file(self):
        return self.type == File.Type.file

    def _set_is_file(self, value):
        assert value, 'Cannot disable `is_file` without another value'
        self.type = File.Type.file

    is_file = property(_get_is_file, _set_is_file)

    @property
    def parent_name(self):
        return os.path.split(os.path.split(self.path.rstrip('/'))[0])[-1]

    def get_revision(self):
        return self.revision_set.filter(deleted__isnull=True)[0]

    def save(self, *args, **kwargs):
        # Make sure directories always have a trailing slash.
        # Weirdly enough the Dropbox API is inconsistent in this, it expects
        # trailing slashes to be used when accessing the API but it does not
        # return trailing slashes.
        if self.is_directory and not self.path.endswith('/'):
            self.path += '/'

        # Make sure we also store the name without the path
        self.name = os.path.split(self.path.rstrip('/'))[-1]

        if not self.pk:
            return super(File, self).save(*args, **kwargs)

        parent = self.parent
        while parent:
            self.tags.add(*parent.tags.all())
            parent = parent.parent

        return super(File, self).save(*args, **kwargs)

    class Meta:
        unique_together = 'path',
        ordering = ['path']


class Permission(base_models.CreatedAtModelBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    read = models.BooleanField()
    rename = models.BooleanField()
    update = models.BooleanField()
    delete = models.BooleanField()
    file = models.ForeignKey('file')

    class Meta:
        unique_together = (
            ('user', 'file'),
        )

