"""
Django settings for tassle_backend project.

Generated by 'django-admin startproject' using Django 2.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os

from django.core.management.utils import get_random_secret_key

# https://django-environ.readthedocs.io/en/latest/#
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set any default values here
env = environ.Env(
    # Disable Django Debug Mode unless specifically set
    DJANGO_DEBUG=(bool, False),
    # DJANGO_SECRET_KEY=(str, get_random_secret_key()),
    ALLOWED_HOSTS=(list, []),
    DJANGO_SHELL_PLUS=(str, 'ptpython')
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# When creating URLs, how many random characters to use?
#TASSLE_URL_LENGTH = 22

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
SITE_ID = env('DJANGO_SITE_ID', default=1)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DJANGO_DEBUG')
SHELL_PLUS = env('DJANGO_SHELL_PLUS')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
AUTH_USER_MODEL = 'restapi.User'
COGNITO_USER_MODEL = 'restapi.User'

## AWS Cognito Backend Config
# https://github.com/labd/django-cognito-jwt
COGNITO_AWS_REGION = env('COGNITO_AWS_REGION', default='us-east-1')
COGNITO_USER_POOL = env('COGNITO_USER_POOL', default='SETME')
COGNITO_AUDIENCE = env('COGNITO_AUDIENCE', default='SETME')  # '6xilpe202urdj8bfe8rgcn7jml'
# Application definition

# Corsheaders
# https://github.com/adamchainz/django-cors-headers
CORS_ALLOWED_ORIGINS = ()
CORS_ALLOWED_ORIGIN_REGEXES = []
CORS_ALLOW_ALL_ORIGINS = True

## Django-storages
# https://django-storages.readthedocs.io/en/latest/
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_STORAGE_BUCKET_NAME')

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# Default to standard django sqlite file DB if environment variable not set

# Use default sqlite3 database unless you have DATABASE_URL environment set
try:
    #DATABASES = {'default': {}}
    DATABASES = {'default': env.db()}
except environ.ImproperlyConfigured:
    DATABASES = {'default': environ.Env().db_url_config('sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))}
#
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
# }
#

INSTALLED_APPS = [
    'grappelli',
    'restapi',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'django_extensions',
    'django_cognito_jwt',
    'corsheaders',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'django_cognito_jwt.JSONWebTokenAuthentication'
    ]
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tassle_backend.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'tassle_backend.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
