"""
Models for actual Polling Stations and Polling Districts!
"""
import urllib.parse
from datetime import datetime
from itertools import groupby

from core.opening_times import OpeningTimes
from django.contrib.gis.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import JSONField
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from uk_geo_utils.helpers import Postcode


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
        index_together = [
            ["council", "internal_council_id"],
            ["council", "polling_district_id"],
        ]

    def __str__(self):
        return "{0} ({1})".format(self.internal_council_id, self.council)

    @property
    def formatted_address(self):
        if not self.address:
            return None
        return "\n".join([x[0].strip() for x in groupby(self.address.split(","))])


class CustomFinderManager(models.Manager):
    def get_custom_finder(self, geocoder, postcode):
        try:
            from addressbase.models import UprnToCouncil

            eoni_data_in_db = UprnToCouncil.objects.filter(
                uprn__postcode__startswith="BT"
            )[:1]

            code = geocoder.get_code("lad")
            if code.startswith("N") and not eoni_data_in_db:
                finder = self.get(pk="N07000001")
                finder.message = _(finder.message)
                """
                EONI's poling station finder requires postcode to have a space :(
                http://www.eoni.org.uk/Offices/Postcode-Search-Results?postcode=BT5+7TQ
                will produce a result, whereas
                http://www.eoni.org.uk/Offices/Postcode-Search-Results?postcode=BT57TQ
                will not.

                We might need to take a more sophisticated approach as we add more custom finders
                that accept postcodes (e.g: a postcode format flag in the database).
                At the moment I only have this one to work with.
                """
                finder.encoded_postcode = urllib.parse.quote(
                    Postcode(postcode).with_space
                )
            else:
                finder = self.get(pk=code)

            return finder
        except ObjectDoesNotExist:
            return None


class CustomFinder(models.Model):
    """
    Store details of areas that have their own
    custom polling station finders
    and/or a message that we might want to show.


    Example content:

    record = CustomFinder(
        area_code='E07000082'
        base_url='https://stroud.maps.arcgis.com/apps/webappviewer/index.html?id=ea6bf4b3655542c1a05c8d7e87d32bb1'
        can_pass_postcode=False
        message="Stroud District Council has its own polling station finder:"
    )
    record.save()

    record = CustomFinder(
        area_code='W06000008'
        base_url=''
        can_pass_postcode=False
        message='<h2>We're working on it!</h2>Ceredigion Council have provided polling station data. It will be available soon.'
    )
    record.save()

    record = CustomFinder(
        area_code='N07000001'
        base_url='http://www.eoni.org.uk/Offices/Postcode-Search-Results?postcode='
        can_pass_postcode=True
        message='The Electoral Office of Northern Ireland has its own polling station finder:'
    )
    record.save()
    """

    area_code = models.CharField(
        max_length=9, primary_key=True, help_text="The GSS code for this area"
    )
    base_url = models.CharField(
        blank=True,
        max_length=255,
        help_text="The landing page for the polling station finder",
    )
    can_pass_postcode = models.BooleanField(
        default=False, help_text="Does the URL have '?postcode=' in it?"
    )
    message = models.TextField(
        blank=True, default="This council has its own polling station finder:"
    )

    objects = CustomFinderManager()


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
