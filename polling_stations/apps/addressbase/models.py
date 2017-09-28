from django.contrib.gis.db import models
from uk_geo_utils.models import AbstractAddress


class AddressManager(models.GeoManager):
    def postcodes_for_district(self, district):
        qs = self.filter(location__within=district.area)
        qs = qs.values_list('postcode', flat=True).distinct()
        return list(qs)

    def points_for_postcode(self, postcode):
        qs = self.filter(postcode=postcode)
        qs = qs.values_list('location', flat=True)
        return list(qs)


class Address(AbstractAddress):
    objects = AddressManager()


class Blacklist(models.Model):
    """
    Model for storing postcodes containing UPRNs in >1 local authorities
    This is intentionally de-normalised for performance reasons
    Ideally ('postcode', 'lad') should be a composite PK,
    but django's ORM doesn't support them.
    """
    postcode = models.CharField(blank=False, max_length=15, db_index=True)
    lad = models.CharField(blank=False, max_length=9)

    class Meta:
        unique_together = (('postcode', 'lad'))
