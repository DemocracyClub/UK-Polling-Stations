import os

from django.db.models import Q

from councils.models import Council, UserCouncils
from polling_stations.db_routers import get_logger_db_name

LOGGER_DB_NAME = get_logger_db_name()


def get_domain(request):
    return os.environ.get("APP_DOMAIN", request.META.get("HTTP_HOST"))


def assign_councils_to_user(user):
    """
    Adds rows to the join table between User and Council
    """
    email_domain = user.email.rsplit("@", 1)[1]
    councils = Council.objects.using(LOGGER_DB_NAME).filter(
        Q(electoral_services_email__contains=email_domain)
        | Q(registration_email__contains=email_domain)
    )

    for council in councils:
        UserCouncils.objects.using(LOGGER_DB_NAME).update_or_create(
            user=user, council=council
        )
