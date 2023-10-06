"""
Django settings for geokey project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

ALLOWED_HOSTS = ['*','127.0.0.1','54.235.229.15']


# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',

    'django_hosts',
    'django_assets',
    'crispy_forms',
    'geoposition',
    'honeypot',
    'argonauts',
    'rest_framework',
#    'social_django',

    'rest_framework.authtoken',

    'debug_toolbar',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'geokey.apikey.APIKeyMiddleware',
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
    'django-webapp.middleware.UUIDValidateMiddleware',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
#        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

SOCIAL_AUTH_URL_NAMESPACE = 'social'

ROOT_URLCONF = 'geokey.urls'

ROOT_HOSTCONF = 'geokey.hosts'
DEFAULT_HOST = 'frontpage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #OAuth
#                'social_django.context_processors.backends',
#                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)

#Facebook OAuth2
SOCIAL_AUTH_FACEBOOK_KEY = '503521843142629'
SOCIAL_AUTH_FACEBOOK_SECRET = '09d7f9b080672d556f93eb025824e448'

# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook. Email is not sent by default, to get it, you must request the email permission:
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

# Google OAuth2
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '657431177107-ke3nid8f6h51fqkv1s5vdcem9j4cei3g.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'qb76AqpWgxCnwa-4J7Sckzha'
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]


WSGI_APPLICATION = 'geokey.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder'
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'main/static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'usergeokey'
SOCIAL_LOGIN_REDIRECT_URL = 'socialauthcomplete'
NATIVE_APP_REDIRECT_URL = 'geokey://app.geokey.io'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

INTERNAL_IPS = ['127.0.0.1', ]


ACCOUNT_ACTIVATION_BASE = 0.0000115740  # 1 second in a day
ACCOUNT_ACTIVATION_DAYS = ACCOUNT_ACTIVATION_BASE * 60 * 30


GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyA-s6jGddt7n87pPV0XUoOb-TXflxGQGAQ'

GEOPOSITION_MAP_OPTIONS = {
    'minZoom': 3,
    'maxZoom': 20,
    'center': {'lat': 35.9132, 'lng': -79.05584},
    'zoom': 6
}

GEOPOSITION_MARKER_OPTIONS = {
    'cursor': 'move',
    'position': {'lat': 35.9132, 'lng': -79.05584}
}

HONEYPOT_FIELD_NAME = 'town'

MAX_GEOKEYS_FOR_FREE_ACCOUNT = 100

DEFAULT_FROM_EMAIL = 'smdye@outlook.com'

SECRET_KEY = '5ipy4%ju1o%v!v%)47gdt2vd=3a_e0-*=fh4+dk@on_3+!d5c%'
DEBUG = True
