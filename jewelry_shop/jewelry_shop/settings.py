"""
Django settings for jewelry_shop project.
Clean and organized with PostgreSQL and Cloudinary setup.
"""

import os
from pathlib import Path
import cloudinary

# -----------------------------
# Custom User Model
# -----------------------------
AUTH_USER_MODEL = "accounts.CustomUser"

# -----------------------------
# Base Directory
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Security
# -----------------------------
SECRET_KEY = 'django-insecure-=(*&j(usdk)w194&^qj+fvg^k5c&wys7i%8g#gq$-@)sn-6%a6'
DEBUG = True  # Set False in production
ALLOWED_HOSTS = ['*']

# -----------------------------
# Installed Apps
# -----------------------------
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your apps
    'shop',
    'cart',
    'orders',
    'accounts',
    'core',
    'adminpanel',

    # Third-party apps
    'cloudinary',
    'cloudinary_storage',
]

# RAZOR PAY

# settings.py

RAZORPAY_KEY_ID = "rzp_test_RBwsaOTbD2OwyW"
RAZORPAY_KEY_SECRET = "R8q75A7759hCA1mpS4ewGo9C"


# -----------------------------
# Authentication Backends
# -----------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # default
]

# -----------------------------
# Middleware
# -----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------
# URL Configuration
# -----------------------------
ROOT_URLCONF = 'jewelry_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'jewelry_shop.wsgi.application'

# -----------------------------
# Database (PostgreSQL Neon)
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_9bz1lLNZeWxC',
        'HOST': 'ep-jolly-term-ada7dbtr-pooler.c-2.us-east-1.aws.neon.tech',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
            'channel_binding': 'require'
        }
    }
}

# -----------------------------
# Password Validation
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# -----------------------------
# Internationalization
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -----------------------------
# Static and Media Files
# -----------------------------

STATICFILES_DIRS = [BASE_DIR / "static"]
# settings.py

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Optional but recommended: compressed + cached files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"  # used for admin but Cloudinary is default storage

# -----------------------------
# Cloudinary Storage
# -----------------------------
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dhol8imhb',
    'API_KEY': '616112266455922',
    'API_SECRET': 'LVW7RCMdSQzSFQHrP5di_K58p4w'
}

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
    secure=True
)

# -----------------------------
# Default primary key field type
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------
# Login Redirects
# -----------------------------
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
