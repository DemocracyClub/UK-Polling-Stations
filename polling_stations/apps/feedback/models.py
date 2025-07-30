import os
from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from polling_stations.settings.constants.asana import AsanaReportType

FOUND_USEFUL_CHOICES = (("YES", _("Yes")), ("NO", _("No")))
VOTE_CHOICES = (
    ("MORE_LIKELY", _("More likely")),
    ("LESS_LIKELY", _("Less likely")),
    ("NO_DIFFERENCE", _("No change")),
)


class Feedback(TimeStampedModel):
    found_useful = models.CharField(
        blank=True, max_length=100, choices=FOUND_USEFUL_CHOICES
    )
    vote = models.CharField(blank=True, max_length=100, choices=VOTE_CHOICES)
    comments = models.TextField(blank=True)
    source_url = models.CharField(blank=True, max_length=800)
    token = models.CharField(blank=True, max_length=100, unique=True)
    asana_url = models.URLField(blank=True)

    def as_asana_object(self):
        desc = truncatechars(self.comments, 30)
        fqdn = os.environ.get("FQDN", "wheredoivote.co.uk")
        base_url = f"https://{fqdn}"
        return {
            "name": f"""{self.pk}: "{desc}" """,
            "projects": [settings.ASANA_PROJECT_ID],
            "custom_fields": {
                settings.ASANA_SITE_LINK_FIELD_ID: urljoin(base_url, self.source_url),
                settings.ASANA_REPORT_LINK_FIELD_ID: urljoin(
                    base_url,
                    reverse(
                        "admin:feedback_feedback_change",
                        kwargs={"object_id": self.pk},
                    ),
                ),
                settings.ASANA_ISSUE_DESCRIPTION_FIELD_ID: self.comments,
                settings.ASANA_REPORT_TYPE_FIELD_ID: AsanaReportType.WDIV_FEEDBACK.value,
            },
        }
