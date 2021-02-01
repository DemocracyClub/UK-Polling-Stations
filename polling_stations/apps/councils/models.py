import re

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

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)

    @property
    def nation(self):
        nations_lookup = {
            "E": "England",
            "W": "Wales",
            "S": "Scotland",
            "N": "Northern Ireland",
        }
        # A GSS code is:
        #   'ANN' + 'NNNNNN' where 'A' is one of 'ENSW' and 'N' is 0-9.
        #   'ANN' section is the Entity Code.
        # We want to look for identifiers that look like GSS codes
        # for the types of organisations that manage elections.

        # Ref: https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=-created&tags=all(PRD_RGC)
        gss_pattern = re.compile(
            """
            ^        # Start of string
            (        # Entity Codes:
                E06   # Unitary Authorities (England)
              | E07   # Non-metropolitan Districts (England)
              | E08   # Metropolitan Districts (England)
              | E09   # London Boroughs (England)
              | N09   # Local Government Districts (Northern Ireland)
              | S12   # Council Areas (Scotland)
              | W06   # Unitary Authorities (Wales)
            )
            [0-9]{6} # id
            $        # End of string
            """,
            re.VERBOSE,
        )
        identifier_matches = [
            identifier
            for identifier in self.identifiers
            if re.match(gss_pattern, identifier)
        ]
        identifier_nations = set(
            nations_lookup[identifier[0]]
            for identifier in identifier_matches
            if identifier
        )
        if len(identifier_nations) == 1:
            return identifier_nations.pop()
        else:
            return ""


class CouncilGeography(models.Model):
    council = models.OneToOneField(
        "Council", related_name="geography", on_delete=models.CASCADE
    )
    gss = models.CharField(blank=True, max_length=20)
    geography = models.MultiPolygonField(null=True)
