from dc_logging_client import DCWidePostcodeLoggingClient

DEBUG = True

SECRET_KEY = "asdasdasdasdasdasdasd"

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

EVERY_ELECTION = {"CHECK": False, "HAS_ELECTION": True}
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}


# To test the DC logging client you must authenticate against the AWS monitoring
# account directly by exporting the AWS creds (or using SSO) and then
# enable the `direct_connection` mode
# from dc_logging_client import DCWidePostcodeLoggingClient
# POSTCODE_LOGGER = DCWidePostcodeLoggingClient(direct_connection=True)
POSTCODE_LOGGER = DCWidePostcodeLoggingClient(fake=True)
