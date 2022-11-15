import os, sys

from dc_logging_client import DCWidePostcodeLoggingClient
from django.utils.translation import gettext_lazy as _

# PATH vars

here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)
repo_root = lambda *x: os.path.join(os.path.abspath(here("../..")), *x)

sys.path.insert(0, root("apps"))


DEBUG = True

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "polling_stations",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "",  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        "PORT": "",  # Set to empty string for default.
    }
}

import dj_database_url

DATABASES["default"] = dj_database_url.config()
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

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
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "data_finder.middleware.UTMTrackerMiddleware",
    "whitelabel.middleware.WhiteLabelMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "pollingstations.middleware.BasicAuthMiddleware",
    "django.middleware.security.SecurityMiddleware",
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
                "dc_signup_form.context_processors.signup_form",
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
    "rest_framework.authtoken",
    "rest_framework_gis",
    "raven.contrib.django.raven_compat",
    "django_extensions",
    "markdown",
    "corsheaders",
    "pipeline",
    "dc_signup_form",
    "apiblueprint_view",
    "dc_design_system",
    "dc_utils",
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

import dc_design_system

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
        "sentry": {
            "level": "ERROR",
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
        },
    },
    "loggers": {
        # Silence DisallowedHost exception by setting null error handler - see
        # https://docs.djangoproject.com/en/1.8/topics/logging/#django-security
        "django.security.DisallowedHost": {"handlers": ["null"], "propagate": False},
        "file_uploads.views": {
            "handlers": ["sentry"],
            "level": "ERROR",
            "propagate": True,
        },
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
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "api.authentication.authentication.TokenAuthSupportQueryString",
    ),
    "DEFAULT_THROTTLE_CLASSES": ("rest_framework.throttling.AnonRateThrottle",),
    "DEFAULT_THROTTLE_RATES": {"anon": "1000/day"},
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

EMBED_PREFIXES = ("embed",)

WHITELABEL_PREFIXES = ()

# CorsMiddleware config
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()
CORS_URLS_REGEX = r"^/(api|embed)/.*$"


INTERNAL_IPS = "127.0.0.1"
SITE_TITLE = _("Where Do I Vote?")
SITE_LOGO = "images/logo_icon.svg"
SITE_LOGO_WIDTH = "390px"

TEST_RUNNER = "django.test.runner.DiscoverRunner"


ADDRESS_MODEL = "addressbase.Address"
ONSUD_MODEL = "addressbase.UprnToCouncil"

EMAIL_SIGNUP_ENDPOINT = "https://democracyclub.org.uk/mailing_list/api_signup/v1/"
EMAIL_SIGNUP_API_KEY = ""


# Disable Basic Auth by default
# We only want to use this on staging deploys
BASICAUTH_DISABLE = True


SHOW_ADVANCE_VOTING_STATIONS = True

# DC Logging Client
POSTCODE_LOGGER = DCWidePostcodeLoggingClient(fake=True)

# settings for load balancer status check
CHECK_SERVER_CLEAN = True
CLEAN_SERVER_FILE = "~/clean"


# import application constants
from .constants.councils import *  # noqa
from .constants.db import *  # noqa
from .constants.directions import *  # noqa
from .constants.elections import *  # noqa
from .constants.importers import *  # noqa
from .constants.tiles import *  # noqa
from .constants.uploads import *  # noqa

# Import .local.py last - settings in local.py override everything else
try:

    from .local import *  # noqa

    try:
        INSTALLED_APPS += PROD_APPS  # noqa
    except NameError:
        pass

except ImportError:
    pass

if DEBUG:
    INSTALLED_APPS += ("dashboard",)

# importing test settings file if necessary (TODO chould be done better)
if len(sys.argv) > 1 and sys.argv[1] in ["test", "harvest"]:
    from .testing import *  # noqa


if os.environ.get("CIRCLECI"):
    from .ci import *  # noqa


# Register Rich as default handler for stacktraces
from rich.traceback import install

install(show_locals=True)
