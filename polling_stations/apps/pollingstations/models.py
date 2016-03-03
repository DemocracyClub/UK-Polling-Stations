"""
Models for actual Polling Stations and Polling Districts!
"""
from django.contrib.gis.db import models

from councils.models import Council


class PollingStation(models.Model):
    council             = models.ForeignKey(Council, null=True)
    internal_council_id = models.CharField(blank=True, max_length=100)
    postcode            = models.CharField(blank=True, null=True, max_length=100)
    address             = models.TextField(blank=True, null=True)
    location            = models.PointField(null=True, blank=True)

    objects = models.GeoManager()

    def __str__(self):
        return "{0} ({1})".format(self.internal_council_id, self.council)


class PollingDistrict(models.Model):
    name                = models.CharField(blank=True, null=True, max_length=255)
    council             = models.ForeignKey(Council, null=True)
    internal_council_id = models.CharField(blank=True, max_length=100)
    extra_id            = models.CharField(blank=True, null=True, max_length=100)
    area                = models.MultiPolygonField(null=True, blank=True)
    # This is NOT a FK, as we might not have the polling station aat
    # the point of import
    polling_station_id  = models.CharField(blank=True, max_length=255)

    objects = models.GeoManager()

    def __unicode__(self):
        name = self.name or "Unnamed"
        return "%s (%s)" % (name, self.council)
