"""
Models for actual Polling Stations and Polling Districts!
"""

from itertools import groupby

from django.contrib.gis.db import models

from councils.models import Council


class PollingDistrict(models.Model):
    name                = models.CharField(blank=True, null=True, max_length=255)
    council             = models.ForeignKey(Council, null=True)
    internal_council_id = models.CharField(blank=True, max_length=100)
    extra_id            = models.CharField(blank=True, null=True, max_length=100)
    area                = models.MultiPolygonField(null=True, blank=True)
    # This is NOT a FK, as we might not have the polling station at
    # the point of import
    polling_station_id  = models.CharField(blank=True, max_length=255)

    objects = models.GeoManager()

    def __unicode__(self):
        name = self.name or "Unnamed"
        return "%s (%s)" % (name, self.council)


class PollingStationManager(models.GeoManager):
    def get_polling_station(self, location, council_id):
        try:
            polling_district = PollingDistrict.objects.get(
                area__covers=location)
        except PollingDistrict.DoesNotExist:
            return None

        if polling_district.internal_council_id:
            # always attempt to look up district id in stations table
            station = self.filter(
                polling_district_id=polling_district.internal_council_id,
                council_id=council_id
            )
            if len(station) == 1:
                return station[0]

        if polling_district.polling_station_id:
            # only try to look up station id if it is a sensible value
            station = self.get_polling_station_by_id(
                internal_council_id=polling_district.polling_station_id,
                council_id=council_id
            )
            # if polling_station_id is set and we don't get a station back
            # or it maps to more than one station due to dodgy data
            # do not fall back and attempt point within polygon lookup
            return station
        else:
            # only try a point within polygon lookup
            # if polling_station_id is not set
            station = self.filter(
                location__within=polling_district.area)
            if len(station) == 1:
                return station[0]
            else:
                # make this explicit rather than implied
                return None

    def get_polling_station_by_id(self, internal_council_id, council_id):
        station = self.filter(
            internal_council_id=internal_council_id,
            council_id=council_id
        )
        if len(station) == 1:
            return station[0]
        else:
            return None


class PollingStation(models.Model):
    council             = models.ForeignKey(Council, null=True)
    internal_council_id = models.CharField(blank=True, max_length=100)
    postcode            = models.CharField(blank=True, null=True, max_length=100)
    address             = models.TextField(blank=True, null=True)
    location            = models.PointField(null=True, blank=True)
    # This is NOT a FK, as we might not have the polling district at
    # the point of import
    polling_district_id  = models.CharField(blank=True, max_length=255)

    objects = PollingStationManager()

    def __str__(self):
        return "{0} ({1})".format(self.internal_council_id, self.council)

    @property
    def formatted_address(self):
        return "\n".join([x[0] for x in groupby(self.address.split(','))])


class ResidentialAddress(models.Model):
    address            = models.TextField(blank=True, null=True)
    postcode           = models.CharField(blank=True, null=True, max_length=100, db_index=True)
    council            = models.ForeignKey(Council, null=True)
    polling_station_id = models.CharField(blank=True, max_length=100)
    slug               = models.SlugField(blank=False, null=False, db_index=True, unique=True, max_length=255)


class DataQualityReport(models.Model):
    council            = models.OneToOneField(Council, primary_key=True)
    report             = models.TextField(blank=False, null=False)
