from django.conf import settings
from django.utils.datetime_safe import datetime


def google_analytics(request):
    return {"disable_ga": getattr(settings, "DISABLE_GA", False)}


NEXT_CHARISMATIC_ELECTION_DATES = getattr(
    settings, "NEXT_CHARISMATIC_ELECTION_DATES", []
)
NEXT_CHARISMATIC_ELECTION_DATES = (
    [
        datetime.strptime(date, "%Y-%m-%d").date()
        for date in NEXT_CHARISMATIC_ELECTION_DATES
    ]
    if NEXT_CHARISMATIC_ELECTION_DATES
    else None
)


def global_settings(request):
    return {
        "RAVEN_CONFIG": getattr(settings, "RAVEN_CONFIG", None),
        "SERVER_ENVIRONMENT": getattr(settings, "SERVER_ENVIRONMENT", None),
        "NEXT_CHARISMATIC_ELECTION_DATES": NEXT_CHARISMATIC_ELECTION_DATES,
    }
