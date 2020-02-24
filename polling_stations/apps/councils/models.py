from django.contrib.gis.db import models


class Council(models.Model):
    council_id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(blank=True, max_length=100)
    website = models.URLField(blank=True)
    postcode = models.CharField(blank=True, null=True, max_length=100)
    address = models.TextField(blank=True, null=True)
    area = models.MultiPolygonField(null=True, blank=True, srid=4326)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
