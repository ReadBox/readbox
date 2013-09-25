ReadBox
==============================================================================

A dropbox wrapper with a faster interface and tagging support.

Install
------------------------------------------------------------------------------

1. Get the files

    git clone git@github.com:ReadBox/readbox.git

2. Create a `local_settings.py` with settings like these:

    STATIC_URL = 'http://your_server/static/'
    COMPRESS_URL = STATIC_URL

    DROPBOX_APP_KEY = ...
    DROPBOX_APP_SECRET = ...
    DROPBOX_ACCESS_TYPE = 'dropbox'
    DROPBOX_BASE_PATH = '/'

3. Install the requirements (I would recommend doing this from within a
   virtualenv)

    pip install -r requirements.txt
   
4. Authenticate and sYnc with dropbox:

   ./manage.py authenticate_dropbox
   ./manage.py sync

5. Run!

   ./manage.py runserver

