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

# Stand-in EveryElection ballots for local testing, keyed by council_id, so
# the uploader (and the election-return prototype) can be exercised without
# needing network access to the real EveryElection API. See
# file_uploads.views.get_ee_wrapper.
FAKE_ELECTIONS = {
    "STO": [
        {
            "election_id": "local.stroud.2026-05-07",
            "election_title": "Stroud District Council local election",
            "poll_open_date": "2026-05-07",
            "group_type": None,
            "cancelled": False,
            "replaced_by": None,
            "metadata": None,
            "requires_voter_id": "EA-2022",
        },
    ]
}

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
