"""
Django settings for irekua project.

Generated by 'django-admin startproject' using Django 1.11.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_!(-2l6l2(d#pjv^efr^@#x+8rz9q36wmm7#uucup42bvv=9%s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

AUTH_USER_MODEL = 'database.User'

INSTALLED_APPS = [
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
    'rest',
    'database',
    'rest_framework_swagger',
]

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

ROOT_URLCONF = 'irekua.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('rest', 'templates')],
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

WSGI_APPLICATION = 'irekua.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
try:
    from .db_config import db_config
except ImportError:
    db_config = {}


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DB_NAME', db_config.get('DB_NAME', 'irekua')),
        'USER': os.environ.get('DB_USER', db_config.get('DB_USER', 'irekua')),
        'PASSWORD': os.environ.get('DB_PASSWORD', db_config.get('DB_PASSWORD', 'password')),
        'HOST': os.environ.get('DB_HOST', db_config.get('DB_HOST', 'localhost')),
        'PORT': os.environ.get('DB_PORT', db_config.get('DB_PORT', '5432')),
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

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
try:
    from .static_config import static_config
except ImportError:
    static_config = {}

STATIC_URL = os.environ.get(
    'STATIC_URL',
    static_config.get('STATIC_URL', '/static/'))
STATIC_ROOT = os.environ.get(
    'STATIC_ROOT',
    static_config.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static/')))

MEDIA_URL = os.environ.get(
    'MEDIA_URL',
    static_config.get('MEDIA_URL', '/media/'))
MEDIA_ROOT = os.environ.get(
    'MEDIA_ROOT',
    static_config.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media/')))

# Locale files
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'irekua', 'locale'),
)


# Rest framework settings
# https://www.django-rest-framework.org/tutorial/quickstart/#settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
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
