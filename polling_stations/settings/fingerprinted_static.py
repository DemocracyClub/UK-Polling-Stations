from .base import *

### NOTE:
### This version is not used, any settings here will not actually be used in production!
### See the ansible version for a version which is actually used!


DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATIC_PRECOMPILER_DISABLE_AUTO_COMPILE = True

MIDDLEWARE_CLASSES = (
  'whitenoise.middleware.WhiteNoiseMiddleware',
) + MIDDLEWARE_CLASSES

INSTALLED_APPS = ('whitenoise.runserver_nostatic',) + INSTALLED_APPS

# Since we have to set DEBUG to False to get ManifestStaticFilesStorage to fingerprint the files we need to set this
ALLOWED_HOSTS = ['127.0.0.1' ]
