import contextlib
import os
import sys
from pathlib import Path

import dc_design_system
import requests
from dc_logging_client import DCWidePostcodeLoggingClient
from django.utils.translation import gettext_lazy as _
from rich import traceback

# PATH vars


def here(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)


PROJECT_ROOT = here("..")


def root(*x):
    return os.path.join(os.path.abspath(PROJECT_ROOT), *x)


def repo_root(*x):
    return os.path.join(os.path.abspath(here("../..")), *x)


sys.path.insert(0, root("apps"))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("SECRET_KEY", "asdasdasdasdasdasdasd")

ADMINS = (("DC developers", "developers@democracyclub.org.uk"),)

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "polling_stations",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        "PORT": "",  # Set to empty string for default.
        "CONN_MAX_AGE": 60,
    }
}

# DATABASES["default"] = dj_database_url.config()
# DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    os.environ.get("FQDN", None),
    "localhost",
    "127.0.0.1",
]


def get_ec2_ip():
    token_req = requests.put(
        "http://169.254.169.254/latest/api/token",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
        timeout=2,
    )
    token_req.raise_for_status()
    token_req.text
    ip_req = requests.get(
        "http://169.254.169.254/latest/meta-data/local-ipv4",
        headers={"X-aws-ec2-metadata-token": token_req.text},
        timeout=2,
    )
    ip_req.raise_for_status()
    return ip_req.text


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "Europe/London"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = root("assets", "uploads")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Make this unique, and don't share it with anybody.
SECRET_KEY = "asdasdasdasdasdasdasd"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = root("static")
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (root("assets"), root("../node_modules"))

from dc_utils.settings.pipeline import *  # noqa

from .static_files import PIPELINE, STATICFILES_FINDERS  # noqa

MIDDLEWARE = (
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "data_finder.middleware.UTMTrackerMiddleware",
    "whitelabel.middleware.WhiteLabelMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "dc_utils.middleware.BasicAuthMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [root("templates")],
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.contrib.auth.context_processors.auth",
                "feedback.context_processors.feedback_form",
                "bug_reports.context_processors.bug_report_form",
                "pollingstations.context_processors.google_analytics",
                "pollingstations.context_processors.global_settings",
                "whitelabel.context_processors.base_template",
                "core.context_processors.canonical_url",
                "core.context_processors.site_title",
            ],
        },
    }
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "sesame.backends.ModelBackend",
]

SESAME_MAX_AGE = 60 * 60 * 2
SESAME_ONE_TIME = False
SESAME_TOKEN_NAME = "login_token"

ROOT_URLCONF = "polling_stations.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "polling_stations.wsgi.application"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.gis",
    "rest_framework",
    "rest_framework_gis",
    "django_extensions",
    "corsheaders",
    "pipeline",
    "dc_design_system",
    "dc_utils",
    "drf_spectacular",
)

PROJECT_APPS = (
    "addressbase",
    "api",
    "councils",
    "data_finder",
    "data_importers",
    "feedback",
    "file_uploads",
    "pollingstations",
    "polling_stations",
    "bug_reports",
    "uk_geo_utils",
    "whitelabel",
)

INSTALLED_APPS += PROJECT_APPS

PIPELINE["SASS_ARGUMENTS"] += " -I " + dc_design_system.DC_SYSTEM_PATH + "/system"

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "ignore_status_checks": {"()": "pollingstations.filters.StatusCheckFilter"},
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false", "ignore_status_checks"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        # Silence DisallowedHost exception by setting null error handler - see
        # https://docs.djangoproject.com/en/1.8/topics/logging/#django-security
        "django.security.DisallowedHost": {"handlers": ["null"], "propagate": False},
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("cy", "Welsh"),
]
USE_I18N = (True,)

LOCALE_PATHS = (repo_root("locale"),)

LOGIN_REDIRECT_URL = "file_uploads:councils_list"
LOGOUT_REDIRECT_URL = "home"

# API Settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.authentication.authentication.HardcodedTokenAuthentication"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


SPECTACULAR_SETTINGS = {
    "TITLE": "WhereDoIVote API",
    "VERSION": "beta",
    "SERVE_INCLUDE_SCHEMA": False,
}
ENABLE_API_DOCS = False

READ_ONLY_API_AUTH_TOKENS = [
    key.strip() for key in os.environ.get("READ_ONLY_API_AUTH_TOKENS", "").split(",")
]
SUPERUSER_API_AUTH_TOKENS = [
    key.strip() for key in os.environ.get("SUPERUSER_API_AUTH_TOKENS", "").split(",")
]

EMBED_PREFIXES = ("embed",)

WHITELABEL_PREFIXES = ()

# CorsMiddleware config
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()
CORS_URLS_REGEX = r"^/(api|embed)/.*$"

INTERNAL_IPS = "127.0.0.1"
SITE_TITLE = _("Where Do I Vote?")
SITE_LOGO = (
    "https://dc-shared-frontend-assets.s3.eu-west-2.amazonaws.com/images/logo_icon.svg"
)
SITE_LOGO_WIDTH = "390px"

TEST_RUNNER = "django.test.runner.DiscoverRunner"

ADDRESS_MODEL = "addressbase.Address"
ONSUD_MODEL = "addressbase.UprnToCouncil"

DEFAULT_FROM_EMAIL = "pollingstations@democracyclub.org.uk"

# Allowlist of URLs that should be ignored by dc_utils BasicAuthMiddleware
BASIC_AUTH_ALLOWLIST = [
    "/status_check/",  # load balancer health check
    "/api",
    "/api/*",
]

SHOW_ADVANCE_VOTING_STATIONS = True

# settings for load balancer status check
CHECK_SERVER_CLEAN = True
CLEAN_SERVER_FILE = "~/clean"
INITIAL_REPLICATION_COMPLETE_FILE = (
    "/var/www/polling_stations/home/db_replication_complete"
)

# When we're running on AWS
if DC_ENVIRONMENT := os.environ.get("DC_ENVIRONMENT", None):
    if not Path(INITIAL_REPLICATION_COMPLETE_FILE).exists():
        DATABASES["local"] = {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": "polling_stations",
            "USER": "",
            "PASSWORD": "",
            "HOST": "",  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            "PORT": "",  # Set to empty string for default.
            "CONN_MAX_AGE": 60,
        }
        DATABASES["default"] = {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "USER": "postgres",
            "NAME": os.environ.get("RDS_DB_NAME"),
            "PASSWORD": os.environ.get("RDS_DB_PASSWORD"),
            "HOST": os.environ.get("RDS_DB_HOST"),
            "PORT": "5432",
        }

    DATABASES["principal"] = {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "USER": "postgres",
        "NAME": os.environ.get("RDS_DB_NAME"),
        "PASSWORD": os.environ.get("RDS_DB_PASSWORD"),
        "HOST": os.environ.get("RDS_DB_HOST"),
        "PORT": "5432",
    }

    DATABASE_ROUTERS = [
        "polling_stations.db_routers.ReplicationRouter",
    ]

    # Sentry config

    import sentry_sdk
    from sentry_sdk.integrations import django
    from sentry_sdk.integrations.logging import ignore_logger

    ignore_logger("django.security.DisallowedHost")

    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[
            django.DjangoIntegration(),
        ],
        environment=os.environ.get("DC_ENVIRONMENT"),
        traces_sample_rate=0,
    )

    # Let's us send emails to users
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_PORT = 587
    EMAIL_HOST = "email-smtp.eu-west-1.amazonaws.com"
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get("SMTP_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD")

    ALLOWED_HOSTS.append(get_ec2_ip())

    USE_X_FORWARDED_HOST = True

    if fqdn := os.environ.get("FQDN"):
        CSRF_TRUSTED_ORIGINS = [
            f"https://{fqdn}",
        ]

    # Logging Client
    LOGGER_ARN = os.environ.get("LOGGER_ARN", None)
    if LOGGER_ARN:
        POSTCODE_LOGGER = DCWidePostcodeLoggingClient(function_arn=LOGGER_ARN)

    INSTALLED_APPS += ("django_dynamodb_cache",)
    CACHES = {
        "default": {
            "BACKEND": "django_dynamodb_cache.backend.DjangoCacheBackend",
            "LOCATION": "wdiv_cache",
            "KEY_FUNCTION": "core.cache.key_function",
            "OPTIONS": {"aws_region_name": "eu-west-2"},
        }
    }

DEBUG_TOOLBAR = False

# import application constants
from .constants.asana import *  # noqa
from .constants.councils import *  # noqa
from .constants.db import *  # noqa
from .constants.directions import *  # noqa
from .constants.elections import *  # noqa
from .constants.importers import *  # noqa
from .constants.tiles import *  # noqa
from .constants.uploads import *  # noqa


# Import .local.py last - settings in local.py override everything else
# only if we're not testing
try:
    if os.environ.get("DJANGO_SETTINGS_MODULE") != "polling_stations.settings.testing":
        from .local import *  # noqa

    with contextlib.suppress(NameError):
        INSTALLED_APPS += PROD_APPS  # noqa

except ImportError:
    pass

if not os.environ.get("DC_ENVIRONMENT"):
    INSTALLED_APPS += ("dashboard",)
    if DEBUG_TOOLBAR:
        INSTALLED_APPS += ("debug_toolbar",)
        MIDDLEWARE = ("debug_toolbar.middleware.DebugToolbarMiddleware",) + MIDDLEWARE

if os.environ.get("CIRCLECI"):
    from .ci import *  # noqa

# Register Rich as default handler for stacktraces
traceback.install(show_locals=True)
