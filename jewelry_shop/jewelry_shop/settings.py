"""
Django settings for jewelry_shop project.
Clean and organized with PostgreSQL (Neon) + Cloudinary setup.
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
SECRET_KEY = "django-insecure-=(*&j(usdk)w194&^qj+fvg^k5c&wys7i%8g#gq$-@)sn-6%a6"
DEBUG = True  # ⚠️ Change to False in production
ALLOWED_HOSTS = ["*"]

# -----------------------------
# Installed Apps
# -----------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "cloudinary_storage",
    "cloudinary",

    # Project apps
    "shop",
    "cart",
    "orders",
    "accounts",
    "core",
    "adminpanel",
]

# -----------------------------
# Razorpay
# -----------------------------
RAZORPAY_KEY_ID = "rzp_test_RBwsaOTbD2OwyW"
RAZORPAY_KEY_SECRET = "R8q75A7759hCA1mpS4ewGo9C"

# -----------------------------
# Authentication
# -----------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # default
]

# -----------------------------
# Middleware
# -----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------
# URL Configuration
# -----------------------------
ROOT_URLCONF = "jewelry_shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "jewelry_shop.wsgi.application"

# -----------------------------
# Database (PostgreSQL Neon)
# -----------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "neondb",
        "USER": "neondb_owner",
        "PASSWORD": "npg_9bz1lLNZeWxC",
        "HOST": "ep-jolly-term-ada7dbtr-pooler.c-2.us-east-1.aws.neon.tech",
        "PORT": "5432",
        "OPTIONS": {
            "sslmode": "require",
            "channel_binding": "require",
        },
    }
}

# -----------------------------
# Password Validation
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------
# Internationalization
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# -----------------------------
# Static & Media
# -----------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ✅ Cloudinary handles all uploaded media
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

MEDIA_URL = "/media/"
# ❌ Removed MEDIA_ROOT because Cloudinary stores media remotely

# -----------------------------
# Cloudinary Config
# -----------------------------
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "dhol8imhb",
    "API_KEY": "415897242499313",
    "API_SECRET": "ZAV-mNXh1vu5mLSSlZS-amWvK98",
}

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE["CLOUD_NAME"],
    api_key=CLOUDINARY_STORAGE["API_KEY"],
    api_secret=CLOUDINARY_STORAGE["API_SECRET"],
    secure=True,
)

# -----------------------------
# Defaults
# -----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------
# Login Redirects
# -----------------------------
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/signup/"
