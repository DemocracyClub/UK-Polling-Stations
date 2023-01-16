from dc_logging_client import DCWidePostcodeLoggingClient

STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "polling_stations",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

POSTCODE_LOGGER = DCWidePostcodeLoggingClient(fake=True)
