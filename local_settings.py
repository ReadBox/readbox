
DROPBOX_APP_KEY = 'k0x97c9dl6wxh3n'
DROPBOX_APP_SECRET = '3cm5yx51es5y9o0'
DROPBOX_ACCESS_TYPE = 'dropbox'
DROPBOX_BASE_PATH = '/Q3 Books/'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'readbox',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'rick',
        'PASSWORD': 'MIb8LkG2UN1LfJwh',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '6432',                      # Set to empty string for default.
        'OPTIONS': {
            'autocommit': True,
        },
    }
}
