from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

FOUND_USEFUL_CHOICES = (("YES", _("Yes")), ("NO", _("No")))
VOTE_CHOICES = (("YES", _("Yes")), ("NO", _("No")))


class Feedback(TimeStampedModel):
    found_useful = models.CharField(
        blank=True, max_length=100, choices=FOUND_USEFUL_CHOICES
    )
    vote = models.CharField(blank=True, max_length=100, choices=VOTE_CHOICES)
    comments = models.TextField(blank=True)
    source_url = models.CharField(blank=True, max_length=800)
    token = models.CharField(blank=True, max_length=100, unique=True)
    asana_url = models.URLField(blank=True)
