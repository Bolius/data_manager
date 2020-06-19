"""
  A Settings file for django that conforms to the principles of a 12factor app.
  It uses django-environ to accomplish this.

  The file starts with reading all enviroment variables, and then configures
  the settings.
"""
import os

import dj_database_url
import raven
from environs import Env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG")
TEMPLATE_DEBUG = DEBUG

# App constants
GEO_KEY = env.str("GEO_KEY")
SECRET_KEY = env.str("SECRET_KEY")
ADMINS = eval(os.environ["ADMINS"])
MANAGERS = eval(os.environ["MANAGERS"])

email = env.dj_email_url("EMAIL_URL")
EMAIL_BACKEND = email["EMAIL_BACKEND"]
EMAIL_HOST = email["EMAIL_HOST"]
EMAIL_HOST_USER = email["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = email["EMAIL_HOST_PASSWORD"]
EMAIL_FILE_PATH = BASE_DIR
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_PORT = email["EMAIL_PORT"]
EMAIL_USE_SSL = email["EMAIL_USE_SSL"]
DEFAULT_FROM_EMAIL = SERVER_EMAIL

ALLOWED_HOSTS = eval(os.environ["ALLOWED_HOSTS"])

if "http://" in os.environ["SENTRY_DSN"]:  # Check if url
    RAVEN_CONFIG = {
        "dsn": os.environ["SENTRY_DSN"],
        "release": raven.fetch_git_sha(BASE_DIR),
    }

# START OF UNIVERSAL SETTINGS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django_extensions",
    "django.contrib.messages",
    "django.contrib.gis",
    "django.contrib.staticfiles",
    "data_models",
    "corsheaders",
    "raven.contrib.django.raven_compat",
    "graphene_django",
    "django_plotly_dash.apps.DjangoPlotlyDashConfig",
]

MIDDLEWARE = [
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_plotly_dash.middleware.BaseMiddleware",
]
# CORS_ORIGIN_WHITELIST = ("localhost:3000", "*", "ml.bolius.dk", "bolius.dk")
ROOT_URLCONF = "data_store.urls"
CORS_ORIGIN_ALLOW_ALL = True
X_FRAME_OPTIONS = "SAMEORIGIN"
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
            ]
        },
    }
]

WSGI_APPLICATION = "data_store.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


DATABASES = {"default": dj_database_url.parse(os.environ["DATABASE_URL"])}

LANGUAGE_CODE = "da-dk"
TIME_ZONE = "Europe/Copenhagen"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


GRAPHENE = {"SCHEMA": "data_models.schema.schema"}

EXPLORATION_QUERY = ""
with open("assets/data_exploration_query.graphql", "r") as queryfile:
    EXPLORATION_QUERY = "".join(queryfile.readlines())


META_QUERY = ""
with open("assets/data_exploration_info_query.graphql", "r") as queryfile:
    META_QUERY = "".join(queryfile.readlines())
