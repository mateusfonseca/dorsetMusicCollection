# CA3: Test and Security

"""
This file defines the settings for the fake CDN only.
Because the CDN is meant to work as if it was in a different server
and with an independent domain.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# CDN domain
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'cdn.dmc.net', ]

# It requires staticfiles in order to server media files and sslserver in order
# to handle HTTPS requests
INSTALLED_APPS = ['django.contrib.staticfiles', 'cdn.apps.CdnConfig', 'sslserver', ]

# Root url different from the main website
ROOT_URLCONF = 'cdn.urls'

WSGI_APPLICATION = 'dorsetMusicCollection.wsgi.application'

# Serves media files at this url
STATIC_URL = 'media/'
# Media files to be served are stored at this path
STATICFILES_DIRS = [BASE_DIR / os.path.join('static', 'cdn'), ]
