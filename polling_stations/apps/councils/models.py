from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


class Council(models.Model):
    council_id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(blank=True, max_length=255)
    identifiers = ArrayField(models.CharField(max_length=100), default=list)

    electoral_services_email = models.EmailField(blank=True)
    electoral_services_phone_numbers = ArrayField(
        models.CharField(max_length=100), default=list
    )
    electoral_services_website = models.URLField(blank=True)
    electoral_services_postcode = models.CharField(
        blank=True, null=True, max_length=100
    )
    electoral_services_address = models.TextField(blank=True, null=True)

    registration_email = models.EmailField(blank=True)
    registration_phone_numbers = ArrayField(
        models.CharField(blank=True, max_length=100), default=list
    )
    registration_website = models.URLField(blank=True)
    registration_postcode = models.CharField(blank=True, null=True, max_length=100)
    registration_address = models.TextField(blank=True, null=True)

    area = models.MultiPolygonField(null=True, blank=True, srid=4326)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
