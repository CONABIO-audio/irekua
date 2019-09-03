"""
Django settings for irekua project.

Generated by 'django-admin startproject' using Django 1.11.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import configparser


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Load private configurations
PRIVATE_CONFIGS = configparser.ConfigParser()
PRIVATE_CONFIGS.read(
    os.path.join(BASE_DIR, 'main', 'config', 'db.ini'),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_!(-2l6l2(d#pjv^efr^@#x+8rz9q36wmm7#uucup42bvv=9%s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Application definition
AUTH_USER_MODEL = 'database.User'
DIRS = []
INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.gis',
    'django.contrib.admindocs',
    'django_filters',
    'rest_framework',
    'widget_tweaks',
    'bootstrap4',
    'crispy_forms',
    'leaflet',
    'database',
    'selia',
    'rest',
    'registration',
    'irekua',
    'irekua_utils',
    'file_handler',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get(
            'DB_NAME',
            PRIVATE_CONFIGS.get('database', 'DB_NAME', fallback='irekua')),
        'USER': os.environ.get(
            'DB_USER',
            PRIVATE_CONFIGS.get('database', 'DB_USER', fallback='irekua')),
        'PASSWORD': os.environ.get(
            'DB_PASSWORD',
            PRIVATE_CONFIGS.get('database', 'DB_PASSWORD', fallback='password')),
        'HOST': os.environ.get(
            'DB_HOST',
            PRIVATE_CONFIGS.get('database', 'DB_HOST', fallback='localhost')),
        'PORT': os.environ.get(
            'DB_PORT',
            PRIVATE_CONFIGS.get('database', 'DB_PORT', fallback='5432')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Locale files
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'main', 'locale'),
)


# Rest framework settings
# https://www.django-rest-framework.org/tutorial/quickstart/#settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest.pagination.StandardResultsSetPagination',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_METADATA_CLASS': 'rest.metadata.CustomMetadata',
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'rest.exception_handler.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'rest.utils.schemas.CustomSchema'
}

# Email configurations
EMAIL = 'selia@conabio.gob.mx'
