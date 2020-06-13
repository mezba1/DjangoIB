import os

import dj_database_url

# Environment

IS_PROD = os.getenv('PY_ENV', 'development') == 'production'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

SECRET_KEY = os.getenv('SECRET_KEY', 'bhzoe9iftd4wzv+dwfgsv-(gss4-v07j@okd0o5i=$eba(#)kg')

DEBUG = not IS_PROD

if IS_PROD:
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
else:
    ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'authentication',
    'boards',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangoib.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'djangoib.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'djangoib.context_processors.defaults',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoib.wsgi.application'


# Database

DATABASES = {
    'default': dj_database_url.config(default='postgres://postgres:postgres@db/djangoib')
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Imgur settings

IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')


# Misc.

ADMINS = [
    ('admin', 'admin@example.com'),
]

ADMIN_INITIAL_PASSWORD = os.getenv('ADMIN_INITIAL_PASSWORD', 'admin')

APP_INFO = os.getenv(
    'APP_INFO',
    'DjangoIB is an image-based bulletin board where you can post comments and share images. '
    'There are boards dedicated to a variety of topics. You do not need to register an account '
    'before participating in the community. Feel free to click on a board below that interests '
    'you and jump right in!'
)

APP_LOGO = os.getenv('APP_LOGO')

APP_NAME = os.getenv('APP_NAME', 'DjangoIB')

COPYRIGHT_TEMPLATE = os.getenv('COPYRIGHT_TEMPLATE', '&copy; {CURRENT_YEAR} {APP_NAME}. All rights reserved.')

CSRF_COOKIE_SECURE = IS_PROD

GA_TRACKING_ID = os.getenv('GA_TRACKING_ID')

MAX_THREADS_PER_PAGE = 10  # Maximum number of threads to show per page

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

SECURE_HSTS_INCLUDE_SUBDOMAINS = IS_PROD

SECURE_HSTS_PRELOAD = IS_PROD

SECURE_HSTS_SECONDS = 60 if IS_PROD else 0

SECURE_REFERRER_POLICY = ['origin-when-cross-origin']

SECURE_SSL_REDIRECT = IS_PROD

SESSION_COOKIE_SECURE = IS_PROD
