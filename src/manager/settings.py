"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1byqgc*=u%-5s!r_-cvde=+4xc08e-1-y%)!w9-zo*korzgwq%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['centos']

# Application definition

INSTALLED_APPS = [
    'deploy',
    'pillars',
    'asset',
    'projects',
    'users',
    'inventory',
    'rest_framework',
    'django_filters',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    # 'DEFAULT_METADATA_CLASS': 'manager.utils.FMetadata',
    'DEFAULT_PAGINATION_CLASS': 'manager.utils.FPagination',
    'PAGE_SIZE': 20
}

ROOT_URLCONF = 'manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['web/dist', 'template'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

AUTHENTICATION_BACKENDS = ['manager.utils.FBackend']

WSGI_APPLICATION = 'manager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'flamingos',
        'USER': 'flamingos',
        'PASSWORD': 'flamingos',
        'HOST': 'postgres',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "web/dist/static"),
]

# Celery Setting
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'redis://redis:6379/0'

# eMail Setting
MAIL_HOST_SERVER = 'smtp.eamil.com'
MAIL_HOST_PORT = 465
MAIL_ACCOUNT = ''
MAIL_PASSWORD = ''

# Redis Setting
REDIS_HOST_SERVER = 'redis'
REDIS_HOST_PORT = 6379
REDIS_DB = 0

# gitlab
GITLAB_HOST = 'http://git'

# salt master
SALT_MASTER_API_HOST = 'http://master'
SALT_MASTER_API_USER = 'flamingos'
SALT_MASTER_API_PASSWORD = 'flamingos'
SALT_STATE_DIRECTORY = '/opt/run/flamingos/data'

APPEND_SLASH = False

SESSION_COOKIE_HTTPONLY = False
