import os

from councils.models import Council, UserCouncils
from django.db.models import Q

from polling_stations.settings.constants.uploads import CUSTOM_DOMAINS


def get_domain(request):
    return os.environ.get("FQDN", request.META.get("HTTP_HOST"))


# This is a quick fix: Raise a PR to
# update CUSTOM_DOMAINS in
# polling_stations/settings/constants/uploads.py
# with the the actual list of email domains
# and councils, as the need arises.
# TO REMOVE:
# 1) Delete the entry from the CUSTOM_DOMAIN list
# 2) In the admin panel, delete the UserCouncil
# object from the bottom of the Council profile page


def assign_approved_custom_domains(user, email_domain):
    # if email_domain in custom_domains, assign it to the
    # corresponding council, otherwise do nothing
    if email_domain := CUSTOM_DOMAINS.get(email_domain, None):
        for council_id in email_domain:
            council = Council.objects.get(council_id=council_id)
            UserCouncils.objects.update_or_create(user=user, council=council)


def assign_councils_to_user(user):
    """
    Adds rows to the join table between User and Council
    """
    email_domain = user.email.rsplit("@", 1)[1]
    assign_approved_custom_domains(user, email_domain)
    councils = Council.objects.filter(
        Q(electoral_services_email__contains=email_domain)
        | Q(registration_email__contains=email_domain)
    )

    for council in councils:
        UserCouncils.objects.update_or_create(user=user, council=council)
