import os
from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from polling_stations.settings.constants.asana import AsanaReportType

STATUS_CHOICES = (("OPEN", "Open"), ("RESOLVED", "Resolved"))

REPORT_TYPES = (("OTHER", "Other"),)


class BugReport(TimeStampedModel):
    description = models.TextField(
        blank=False,
        verbose_name=_(
            "Provide information about the problem to help us improve our service:"
        ),
    )
    source_url = models.CharField(blank=True, max_length=800)
    status = models.CharField(blank=False, max_length=100, choices=STATUS_CHOICES)
    user_agent = models.TextField(blank=True)
    source = models.CharField(blank=True, max_length=100)
    email = models.EmailField(
        blank=True, max_length=100, verbose_name=_("(Optional) Email address:")
    )
    report_type = models.CharField(blank=False, max_length=100, choices=REPORT_TYPES)
    asana_url = models.URLField(blank=True)

    def as_asana_object(self):
        desc = truncatechars(self.description, 30)
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
                        "admin:bug_reports_bugreport_change",
                        kwargs={"object_id": self.pk},
                    ),
                ),
                settings.ASANA_ISSUE_DESCRIPTION_FIELD_ID: self.description,
                settings.ASANA_REPORT_TYPE_FIELD_ID: AsanaReportType.WDIV_BUG_REPORT.value,
            },
        }
