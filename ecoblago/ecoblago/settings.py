from django.utils.translation import gettext_lazy as _
import os
from pathlib import Path

import dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR.parent.joinpath(".env"))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG_STR = os.getenv("DJANGO_DEBUG").lower()
DEBUG = DEBUG_STR in {"true", "yes", "1", "y", "t"}

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
).split(", ")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authpage.apps.AuthpageConfig",
    "catalog.apps.CatalogConfig",
    "profilepage.apps.ProfilepageConfig",
    "settingspage.apps.SettingspageConfig",
    "sorl.thumbnail",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "login_required.middleware.LoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LOGIN_REQUIRED_IGNORE_PATHS = [
    r"/admin/",
    r"/authpage/",
    r"/media/",
    r"/static/",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

if DEBUG:
    INSTALLED_APPS += (
        "debug_toolbar",
    )

    MIDDLEWARE += (
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )


ROOT_URLCONF = "ecoblago.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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

WSGI_APPLICATION = "ecoblago.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = "authpage:authpage"

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
    ("kk", _("Kazakh")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

USE_I18N = True

TIME_ZONE = "UTC"

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static/",
]

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'authpage.User'

FIXTURE_DIRS = [
    BASE_DIR / "fixtures/",
]
