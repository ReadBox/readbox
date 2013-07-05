import sys
# Very ugly hack but we only want this monkey patching within this management
# command and it has to be early...
if sys.argv == ['./manage.py', 'sync']:
    import eventlet
    eventlet.monkey_patch()

from django_utils.management.commands import base_command
import optparse
from readbox import dropbox

class Command(base_command.CustomBaseCommand):
    loggers = base_command.CustomBaseCommand.loggers + (
        'readbox.dropbox',
    )
    option_list = base_command.CustomBaseCommand.option_list + (
        optparse.make_option('-n', '--no-cache', action='store_true',
            help='Force a full refresh of all files. Should only be used if '
            'the database models or Dropbox API changed in such a way that a '
            'normal sync will not suffice.'),
        optparse.make_option('-t', '--threads', type='int',
            help='The amount of concurrent download threads to use',
            default=10),
    )

    def handle(self, threads=1, no_cache=False, *args, **kwargs):
        base_command.CustomBaseCommand.handle(self, *args, **kwargs)

        dropbox.Syncer(
            force=no_cache,
            threads=threads,
        ).start()

