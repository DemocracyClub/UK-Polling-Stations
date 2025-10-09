import os

from dc_logging_client import DCWidePostcodeLoggingClient

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "pipeline.storage.PipelineStorage"},
}

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "USER": os.environ.get("CI_DB_USER", "postgres"),
        "NAME": os.environ.get("CI_DB_NAME", "polling_stations"),
        "PASSWORD": os.environ.get("CI_DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("CI_DB_HOST", ""),
        "PORT": "5432",
    }
}

POSTCODE_LOGGER = DCWidePostcodeLoggingClient(fake=True)
