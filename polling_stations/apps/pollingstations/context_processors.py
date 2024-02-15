from datetime import datetime

from django.conf import settings


def google_analytics(request):
    return {"disable_ga": getattr(settings, "DISABLE_GA", False)}


NEXT_CHARISMATIC_ELECTION_DATES = getattr(
    settings, "NEXT_CHARISMATIC_ELECTION_DATES", []
)
NEXT_CHARISMATIC_ELECTION_DATES.sort()
NEXT_CHARISMATIC_ELECTION_DATE = (
    datetime.strptime(NEXT_CHARISMATIC_ELECTION_DATES[0], "%Y-%m-%d").date()
    if NEXT_CHARISMATIC_ELECTION_DATES
    else None
)


def global_settings(request):
    return {
        "RAVEN_CONFIG": getattr(settings, "RAVEN_CONFIG", None),
        "SERVER_ENVIRONMENT": getattr(settings, "SERVER_ENVIRONMENT", None),
        "NEXT_CHARISMATIC_ELECTION_DATE": NEXT_CHARISMATIC_ELECTION_DATE,
    }
