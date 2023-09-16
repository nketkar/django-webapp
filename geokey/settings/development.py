import os

from base import BASE_DIR

ALLOWED_HOSTS = ['localhost', 'geokey.loc', 'app.geokey.loc', 'www.geokey.loc']


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5ipy4%ju1o%v!v%)47gdt2vd=3a_e0-*=fh4+dk@on_3+!d5c%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ASSETS_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
