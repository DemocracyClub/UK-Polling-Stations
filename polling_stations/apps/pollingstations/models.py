"""
Models for actual Polling Stations and Polling Districts!
"""

from datetime import datetime
from itertools import groupby

from core.opening_times import OpeningTimes
from django.contrib.gis.db import models
from django.db.models import CheckConstraint, JSONField, Q
from django.utils.functional import cached_property
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django_extensions.db.models import TimeStampedModel


class PollingDistrict(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255)
    council = models.ForeignKey("councils.Council", null=True, on_delete=models.CASCADE)
    internal_council_id = models.CharField(blank=True, max_length=100)
    extra_id = models.CharField(blank=True, null=True, max_length=100)
    area = models.MultiPolygonField(null=True, blank=True)
    # This is NOT a FK, as we might not have the polling station at
    # the point of import
    polling_station_id = models.CharField(blank=True, max_length=255)

    class Meta:
        unique_together = ("council", "internal_council_id")

    objects = models.Manager()

    def __unicode__(self):
        name = self.name or "Unnamed"
        return "%s (%s)" % (name, self.council)


class VisibilityChoices(models.TextChoices):
    # Visible on website and in API.
    PUBLISHED = "PUBLISHED", "Published"
    # Only visible to upload user and admin. I.e. not on website or API.
    UNPUBLISHED = "UNPUBLISHED", "Unpublished"


class PollingStation(models.Model):
    council = models.ForeignKey(
        "councils.Council", null=True, db_index=True, on_delete=models.CASCADE
    )
    internal_council_id = models.CharField(
        blank=True,
        max_length=100,
        db_index=True,
        help_text="An id used by the council that is not persistent between elections",
    )
    postcode = models.CharField(blank=True, null=True, max_length=100)
    address = models.TextField(blank=True, null=True)
    location = models.PointField(null=True, blank=True)
    # This is NOT a FK, as we might not have the polling district at
    # the point of import
    polling_district_id = models.CharField(blank=True, max_length=255)
    visibility = models.CharField(
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLISHED,
        help_text="""
            Determines visibility level of a station.<br>
            Whatever this value is set to will persist when an import script is rerun, as long as there isn't a new file
            from the council.<br>
            If there has been a new file, then all stations in that file will default to 'published'.<br>
            This means you need to remember if you want a station to be republished or stay unpublished.
        """,
    )

    class Meta:
        unique_together = ("council", "internal_council_id")
        indexes = [
            models.Index(fields=["council", "internal_council_id"]),
            models.Index(fields=["council", "polling_district_id"]),
        ]

    def __str__(self):
        return "{0} ({1})".format(self.internal_council_id, self.council)

    @property
    def formatted_address(self):
        if not self.address:
            return None
        return "\n".join(
            [x[0].strip().replace("`", "'") for x in groupby(self.address.split(","))]
        )


class AccessibilityInformation(TimeStampedModel):
    polling_station = models.OneToOneField(
        PollingStation,
        on_delete=models.CASCADE,
        related_name="accessibility_information",
    )
    is_temporary = models.BooleanField(null=True)
    nearby_parking = models.BooleanField(null=True)
    disabled_parking = models.BooleanField(null=True)
    level_access = models.BooleanField(null=True)
    temporary_ramp = models.BooleanField(null=True)
    hearing_loop = models.BooleanField(null=True)
    public_toilets = models.BooleanField(null=True)
    getting_to_the_station = models.TextField(blank=True, null=True)
    getting_to_the_station_cy = models.TextField(blank=True, null=True)
    at_the_station = models.TextField(blank=True, null=True)
    at_the_station_cy = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            CheckConstraint(
                name="no_ramp_if_access_level",
                condition=~Q(Q(level_access=True) & Q(temporary_ramp=True)),
            )
        ]

    @property
    def has_at_station_info(self):
        return any(
            [
                self.is_temporary,
                self.nearby_parking,
                self.disabled_parking,
                self.level_access,
                self.temporary_ramp,
                self.hearing_loop,
                self.public_toilets,
                self.at_the_station,
            ]
        )

    @cached_property
    def level_access_text(self):
        if self.level_access is None:
            return None
        if self.level_access:
            return _("level access")
        if not self.level_access and self.temporary_ramp:
            return _("a temporary ramp for access")
        if not self.level_access and not self.temporary_ramp:
            return _("a ramp for access")
        return None

    @cached_property
    def at_the_station_text(self):
        if get_language() == "cy":
            return self.at_the_station_cy
        return self.at_the_station

    @cached_property
    def getting_to_the_station_text(self):
        if get_language() == "cy":
            return self.getting_to_the_station_cy
        return self.getting_to_the_station


class AdvanceVotingStation(models.Model):
    name = models.CharField(max_length=100)
    postcode = models.CharField(blank=True, null=True, max_length=100)
    address = models.TextField(blank=True, null=True)
    location = models.PointField(null=True, blank=True)
    opening_times = JSONField(null=True)
    council = models.ForeignKey("councils.Council", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.postcode})"

    def save(self, **kwargs):
        self.address = "\n".join(
            [line.lstrip() for line in self.address.split("\n")]
        ).strip()
        return super().save(**kwargs)

    @cached_property
    def get_opening_times(self):
        return OpeningTimes.from_dict(self.opening_times)

    @property
    def opening_times_table(self):
        return self.get_opening_times.as_table()

    @property
    def open_in_future(self):
        last_open_row = self.opening_times_table[-1]
        last_date, last_open, last_close = last_open_row
        return datetime.combine(last_date, last_close) > datetime.now()
