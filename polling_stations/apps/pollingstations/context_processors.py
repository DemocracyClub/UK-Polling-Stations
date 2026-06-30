from datetime import datetime

from django.conf import settings


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
        "SERVER_ENVIRONMENT": getattr(settings, "SERVER_ENVIRONMENT", None),
        "NEXT_CHARISMATIC_ELECTION_DATE": NEXT_CHARISMATIC_ELECTION_DATE,
    }
