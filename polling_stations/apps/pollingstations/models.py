from django.contrib.gis.db import models

# Create your models here.


class PollingStation(models.Model):
    objects = models.GeoManager()
    postcode = models.CharField(blank=True, null=True, max_length=100)
    address = models.TextField(blank=True, null=True)
    location = models.PointField(null=True, blank=True)


class PollingDistrict(models.Model):
    objects = models.GeoManager()
    name = models.CharField(blank=True, null=True, max_length=255)
    council_id = models.CharField(blank=True, null=True, max_length=100)
    extra_id = models.CharField(blank=True, null=True, max_length=100)
    area = models.MultiPolygonField(null=True, blank=True, geography=True)

    def __unicode__(self):
        return self.name