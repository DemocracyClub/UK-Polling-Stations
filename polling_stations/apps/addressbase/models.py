from django.contrib.gis.db import models
from django.db import connection
from uk_geo_utils.models import (
    AbstractAddress,
    AbstractAddressManager,
    AbstractOnsudManager,
)


class AddressManager(AbstractAddressManager):
    def postcodes_for_district(self, district):
        qs = self.filter(location__within=district.area)
        qs = qs.values_list("postcode", flat=True).distinct()
        return list(qs)

    def points_for_postcode(self, postcode):
        qs = self.filter(postcode=postcode)
        qs = qs.values_list("location", flat=True)
        return list(qs)


class Address(AbstractAddress):
    objects = AddressManager()


class UprnToCouncil(models.Model):
    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "lad",
                ],
                name="lookup_lad_idx",
            )
        ]

    objects = AbstractOnsudManager()
    lad = models.CharField(blank=True, max_length=9)
    uprn = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        primary_key=True,
        max_length=12,
        db_column="uprn",
    )
    polling_station_id = models.CharField(blank=True, max_length=255)


def get_uprn_hash_table(council_id):
    addresses = Address.objects.filter(uprntocouncil__lad=council_id)
    # return result a hash table keyed by UPRN
    return {
        a.uprn: {
            "address": a.address,
            "postcode": a.postcode.replace(" ", ""),
            "location": a.location,
        }
        for a in addresses
    }
