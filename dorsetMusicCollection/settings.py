# CA1: CRUD Application
# CA2: Registration/Authentication
# CA3: Test and Security

"""
This file defines the general settings for the project,
which is shared across multiple apps.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.dorsetmusiccollection.com', ]

# Application definition

# Added sslserver in order to handle HTTPS requests
INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'polls.apps.PollsConfig', 'accounts.apps.AccountsConfig', 'sslserver', ]

MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
              'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware', ]

ROOT_URLCONF = 'dorsetMusicCollection.urls'

TEMPLATES = [
    {'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True,
     'OPTIONS': {'context_processors': ['django.template.context_processors.debug',
                                        'django.template.context_processors.request',
                                        'django.contrib.auth.context_processors.auth',
                                        'django.contrib.messages.context_processors.messages', ], }, }, ]

WSGI_APPLICATION = 'dorsetMusicCollection.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Database credentials set to be read from a local configuration file.
# It might be needed to replace the active block and set the credentials accordingly.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'database',
#         'USER': 'username',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         },
#     }
# }

# Added TEST dictionary as part of the default database, which replicates the main database structure
# and uses it for test purposes.
DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 'OPTIONS': {'read_default_file': '/etc/mysql/my.cnf', },
                         'TEST': {'NAME': 'test_dorset_music_collection'}}}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', }, ]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Dublin'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static", ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"
FIXTURE_DIRS = [BASE_DIR / "fixtures", ]

# Block added for CA3
# Protecting sensitive data
SECURE_SSL_REDIRECT = True  # redirects all non-HTTPS requests to HTTPS
CSRF_COOKIE_SECURE = True  # CSRF cookie is only sent with an HTTPS connection
SESSION_COOKIE_SECURE = True  # session cookie is only sent with an HTTPS connection
# HTTP Strict Transport Security
SECURE_HSTS_SECONDS = 2592000  # browser to refuse to connect via an insecure connection for 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # all subdomains included in the above
SECURE_HSTS_PRELOAD = True  # domain to be submitted to browser preload list
