from django_utils.management.commands import base_command
from dropbox import session
from django.conf import settings
try:
    from cPickle import dump
except:
    from pickle import dump

class Command(base_command.CustomBaseCommand):
    def handle(self, *args, **kwargs):
        sess = session.DropboxSession(
            settings.DROPBOX_APP_KEY,
            settings.DROPBOX_APP_SECRET,
            settings.DROPBOX_ACCESS_TYPE,
        )
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        
        # Make the user sign in and authorize this token
        print 'url: %s' % url
        print 'Please visit this website and press the "Allow" button.'
        print 'After that, hit "Enter" here.'
        raw_input()
        
        # This will fail if the user didn't visit the above URL
        sess.obtain_access_token(request_token)

        with open(settings.DROPBOX_SESSION_FILE, 'wb') as fh:
            dump(sess, fh)

