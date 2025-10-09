from .base import *  # noqa
from dc_logging_client import DCWidePostcodeLoggingClient
import os

EVERY_ELECTION["CHECK"] = True  # noqa
NEXT_CHARISMATIC_ELECTION_DATES = []
DISABLE_GA = True  # don't log to Google Analytics when we are running tests

INSTALLED_APPS = list(INSTALLED_APPS)  # noqa

# MIGRATION_MODULES = {app: None for app in INSTALLED_APPS if "django" not in app}

MAPZEN_API_KEY = ""
GOOGLE_API_KEYS = []
MAPBOX_API_KEY = ""

STORAGES["staticfiles"] = {"BACKEND": "pipeline.storage.PipelineStorage"}  # noqa F405

RUNNING_TESTS = True

POSTCODE_LOGGER = DCWidePostcodeLoggingClient(fake=True)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

READ_ONLY_API_AUTH_TOKENS = [
    "test_token",
]
SUPERUSER_API_AUTH_TOKENS = [
    "superuser-key",
]
