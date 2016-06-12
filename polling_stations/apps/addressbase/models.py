from django.contrib.gis.db import models


class AddressManager(models.GeoManager):
    def postcodes_for_district(self, district):
        qs = self.filter(location__within=district.area)
        qs = qs.values_list('postcode', flat=True).distinct()
        return list(qs)

    def points_for_postcode(self, postcode):
        qs = self.filter(postcode=postcode)
        qs = qs.values_list('location', flat=True)
        return list(qs)


class Address(models.Model):
    uprn = models.CharField(primary_key=True, max_length=100)
    address = models.TextField(blank=True)
    postcode = models.CharField(blank=True, max_length=15, db_index=True)
    location = models.PointField(null=True, blank=True)

    objects = AddressManager()
