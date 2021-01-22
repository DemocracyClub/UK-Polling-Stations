from .base import *  # noqa


EVERY_ELECTION["CHECK"] = True  # noqa
NEXT_CHARISMATIC_ELECTION_DATE = None
DISABLE_GA = True  # don't log to Google Analytics when we are running tests

INSTALLED_APPS = list(INSTALLED_APPS)  # noqa
INSTALLED_APPS.append("aloe_django")

NOSE_ARGS = ["--verbosity=2", "--nologcapture", "--nocapture"]

MIGRATION_MODULES = {app: None for app in INSTALLED_APPS if "django" not in app}

MAPZEN_API_KEY = ""
GOOGLE_API_KEYS = []
