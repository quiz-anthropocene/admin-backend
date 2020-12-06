"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv(verbose=True)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv("DEBUG") == "True":
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = [os.environ["HOST"]]

DOMAIN_URL = "https://quizanthropocene.fr"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "django_extensions",
    "import_export",
    "ckeditor",
    "solo",  # django-solo
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {}
DATABASES["default"] = dj_database_url.config(conn_max_age=600)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"


# CORS

CORS_ORIGIN_WHITELIST = [
    "http://localhost:8080",
    "https://know-your-planet.netlify.com",
    "https://know-your-planet.netlify.app",
    "https://quiztaplanete.fr",
    "https://quizanthropocene.fr",
]

CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https:\/\/deploy-preview-\w+--know-your-planet\.netlify\.app$",
]


# Cookie security

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False if os.getenv("SESSION_COOKIE_SECURE") == "False" else True
CSRF_COOKIE_SECURE = False if os.getenv("CSRF_COOKIE_SECURE") == "False" else True


# SSL security

SECURE_SSL_REDIRECT = False if os.getenv("SECURE_SSL_REDIRECT") == "False" else True
SECURE_HSTS_SECONDS = os.getenv("SECURE_HSTS_SECONDS")


# Django Import Export

IMPORT_EXPORT_SKIP_ADMIN_LOG = True


# Shell Plus

SHELL_PLUS_IMPORTS = [
    "from datetime import datetime, date, timedelta",
    "from api import constants, utilities, utilities_stats, utilities_notion, utilities_github",
]


# Github

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
GITHUB_CRON_ACTION_TOKEN = os.getenv("GITHUB_CRON_ACTION_TOKEN")

# Notion.so

NOTION_TOKEN_V2 = os.getenv("NOTION_TOKEN_V2")
NOTION_QUESTIONS_TABLE_URL = os.getenv("NOTION_QUESTIONS_TABLE_URL")
NOTION_CONTRIBUTION_TABLE_URL = os.getenv("NOTION_CONTRIBUTION_TABLE_URL")
NOTION_IMPORT_STATS_TABLE_URL = os.getenv("NOTION_IMPORT_STATS_TABLE_URL")
NOTION_GLOSSARY_TABLE_URL = os.getenv("NOTION_GLOSSARY_TABLE_URL")


# Sendinblue (Newsletter)

SIB_API_KEY = os.getenv("SIB_API_KEY")
SIB_NEWSLETTER_LIST_ID = os.getenv("SIB_NEWSLETTER_LIST_ID")
SIB_NEWSLETTER_DOI_TEMPLATE_ID = os.getenv("SIB_NEWSLETTER_DOI_TEMPLATE_ID")
SIB_CONTACT_DOI_ENDPOINT = (
    "https://api.sendinblue.com/v3/contacts/doubleOptinConfirmation"
)


# django-ckeditor

CKEDITOR_CONFIGS = {
    "default": {
        "height": 200,
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            ["NumberedList", "BulletedList"],
            ["Link", "Unlink"],
            ["SpecialChar"],
            # ['HorizontalRule', 'Smiley'],
            ["Undo", "Redo"],
            ["RemoveFormat", "Source"],
        ],
        # avoid special characters encoding
        "basicEntities": False,
        "entities": False,
    }
}
