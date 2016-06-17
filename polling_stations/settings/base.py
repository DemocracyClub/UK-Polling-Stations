import os, sys
from os.path import join, abspath, dirname

# PATH vars

here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)
repo_root = lambda *x: join(abspath(here("../..")), *x)

sys.path.insert(0, root('apps'))


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'polling_stations',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

import dj_database_url
DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = root('assets', 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = root('static_root')
# print(STATIC_ROOT)

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    root('assets'),
    root('static'),
)

# TODO find a way to move these in to the DC theme app?
STATIC_PRECOMPILER_ROOT =root('static')
import os
import dc_theme
root_path = os.path.dirname(dc_theme.__file__)
STATIC_PRECOMPILER_COMPILERS = (
    ('static_precompiler.compilers.scss.SCSS', {
        "sourcemap_enabled": True,
        # "output_style": "compressed",
        "load_paths": [
            root_path + '/static/dc_theme/bower_components/foundation-sites/assets',
            root_path + '/static/dc_theme/bower_components/foundation-sites/scss',
            root_path + '/static/dc_theme/bower_components/motion-ui/src',
            root_path + '/static/dc_theme/scss/',
        ],
    }),
)


# Use write-through cache for sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'static_precompiler.finders.StaticPrecompilerFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'asdasdasdasdasdasdasd'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'data_finder.middleware.UTMTrackerModdleware',
    'whitelabel.middleware.WhiteLabelModdleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    'django.core.context_processors.request',
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.contrib.auth.context_processors.auth",
    "whitelabel.context_processors.base_template",
    'dc_theme.context_processors.dc_theme_context'
)


ROOT_URLCONF = 'polling_stations.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'polling_stations.wsgi.application'

TEMPLATE_DIRS = (
    root('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'rest_framework',
    'django_extensions',
)

PROJECT_APPS = (
    'pollingstations',
    'councils',
    'data_finder',
    'data_collection',
    'whitelabel',
    'nus_wales',
    'dc_theme',
    'static_precompiler',
)

INSTALLED_APPS += PROJECT_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

"""
Map config:
-----------

Set a shell environment variable TILE_LAYER
to configure which tile layer is used by leaflet.

Supported values are:
'MapQuestOpen' (default)
'MapQuestSDK'
'OpenStreetMap'
"""
TILE_LAYER = os.environ.get('TILE_LAYER', 'MapQuestOpen')
"""
Set a shell environment variable MQ_KEY
to specify MapQuestSDK API key.
"""
MQ_KEY = os.environ.get('MQ_KEY', None)


from django.utils.translation import ugettext_lazy as _
LANGUAGE_CODE = 'en'
LANGUAGES = [
  ('en', 'English'),
  ('cy-gb', 'Welsh'),
]
USE_I18N = True,
USE_L10N = True,
LOCALE_PATHS = (
    repo_root('locale'),
)


# API Settings

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

EMBED_PREFIXES = (
    'embed',
)

WHITELABEL_PREFIXES = (
    'nus_wales',
)


INTERNAL_IPS = ('127.0.0.1')
SITE_TITLE = "Where Do I Vote?"

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# importing test settings file if necessary (TODO chould be done better)
if len(sys.argv) > 1 and sys.argv[1] in ['test', 'harvest']:
    from .testing import *


