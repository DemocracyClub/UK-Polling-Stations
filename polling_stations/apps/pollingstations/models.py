"""
Models for actual Polling Stations and Polling Districts!
"""

from itertools import groupby
import urllib.parse

from django.contrib.gis.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.translation import ugettext as _

from councils.models import Council
from uk_geo_utils.helpers import Postcode


class PollingDistrict(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255)
    council = models.ForeignKey(Council, null=True, on_delete=models.CASCADE)
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


class PollingStationManager(models.Manager):
    def get_polling_station(self, council_id, location=None, polling_district=None):
        assert any((polling_district, location))

        if not polling_district:
            try:
                polling_district = PollingDistrict.objects.get(area__covers=location)
            except PollingDistrict.DoesNotExist:
                return None
            except PollingDistrict.MultipleObjectsReturned:
                return None

        if polling_district.internal_council_id:
            # always attempt to look up district id in stations table
            station = self.filter(
                polling_district_id=polling_district.internal_council_id,
                council_id=council_id,
            )

            if len(station) == 1:
                return station[0]
            else:
                addresses = set([s.address for s in station])
                if len(addresses) == 1:
                    return station[0]

        if polling_district.polling_station_id:
            # only try to look up station id if it is a sensible value
            station = self.get_polling_station_by_id(
                internal_council_id=polling_district.polling_station_id,
                council_id=council_id,
            )
            # if polling_station_id is set and we don't get a station back
            # or it maps to more than one station due to dodgy data
            # do not fall back and attempt point within polygon lookup
            return station
        else:
            # make this explicit rather than implied
            return None

    def get_polling_station_by_id(self, internal_council_id, council_id):
        station = self.filter(
            internal_council_id=internal_council_id, council_id=council_id
        )
        if len(station) == 1:
            return station[0]
        else:
            return None


class PollingStation(models.Model):
    council = models.ForeignKey(
        Council, null=True, db_index=True, on_delete=models.CASCADE
    )
    internal_council_id = models.CharField(blank=True, max_length=100, db_index=True)
    postcode = models.CharField(blank=True, null=True, max_length=100)
    address = models.TextField(blank=True, null=True)
    location = models.PointField(null=True, blank=True)
    # This is NOT a FK, as we might not have the polling district at
    # the point of import
    polling_district_id = models.CharField(blank=True, max_length=255)

    class Meta:
        unique_together = ("council", "internal_council_id")
        index_together = [
            ["council", "internal_council_id"],
            ["council", "polling_district_id"],
        ]

    objects = PollingStationManager()

    def __str__(self):
        return "{0} ({1})".format(self.internal_council_id, self.council)

    @property
    def formatted_address(self):
        if not self.address:
            return None
        return "\n".join([x[0].strip() for x in groupby(self.address.split(","))])


class ResidentialAddress(models.Model):
    address = models.TextField(blank=True, null=True)
    postcode = models.CharField(blank=True, null=True, max_length=100, db_index=True)
    council = models.ForeignKey(Council, null=True, on_delete=models.CASCADE)
    polling_station_id = models.CharField(blank=True, max_length=100)
    slug = models.SlugField(
        blank=False, null=False, db_index=True, unique=True, max_length=255
    )
    uprn = models.CharField(max_length=100, blank=True)
    location = models.PointField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        strip all whitespace from postcode and convert to uppercase
        this will make it easier to query based on user-supplied postcode
        """
        self.postcode = Postcode(self.postcode).without_space
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("address_view", args=(self.slug,))


class CustomFinderManager(models.Manager):
    def get_custom_finder(self, geocoder, postcode):
        try:
            finder = self.get(pk__in=[geocoder.get_code("lad")])
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
            finder.encoded_postcode = urllib.parse.quote(Postcode(postcode).with_space)

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
