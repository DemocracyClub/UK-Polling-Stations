from django.contrib.gis.db import models

from councils.models import Council


class PollingStation(models.Model):
    council = models.ForeignKey(Council, null=True)
    internal_council_id = models.CharField(blank=True, max_length=100)
    postcode = models.CharField(blank=True, null=True, max_length=100)
    address = models.TextField(blank=True, null=True)
    location = models.PointField(null=True, blank=True)

    objects = models.GeoManager()


class PollingDistrict(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255)
    council = models.ForeignKey(Council, null=True)
    internal_council_id = models.CharField(blank=True, max_length=100)
    extra_id = models.CharField(blank=True, null=True, max_length=100)
    area = models.MultiPolygonField(null=True, blank=True, geography=True)

    objects = models.GeoManager()

    def __unicode__(self):
        name = self.name or "Unnamed"
        return "%s (%s)" % (name, self.council)
