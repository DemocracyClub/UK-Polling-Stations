from django.db import models
from django_extensions.db.models import TimeStampedModel


STATUS_CHOICES = (
    ('OPEN', 'Open'),
    ('RESOLVED', 'Resolved'),
)

REPORT_TYPES = (
    ('OTHER', 'Other'),
)


class BugReport(TimeStampedModel):
    description = models.TextField(
        blank=False,
        verbose_name='Provide information about the problem to help us improve our service:'
    )
    source_url = models.CharField(blank=True, max_length=800)
    status = models.CharField(
        blank=False,
        max_length=100,
        choices=STATUS_CHOICES,
    )
    user_agent = models.TextField(blank=True)
    source = models.CharField(blank=True, max_length=100)
    email = models.EmailField(
        blank=True,
        max_length=100,
        verbose_name='(Optional) Email address:'
    )
    report_type = models.CharField(
        blank=False,
        max_length=100,
        choices=REPORT_TYPES,
    )
