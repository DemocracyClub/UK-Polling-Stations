from django.contrib.gis.db import models
from uk_geo_utils.models import (
    AbstractAddress,
    AbstractOnsudManager,
)

from councils.models import Council
from pollingstations.models import PollingStation


class Address(AbstractAddress):
    def get_council_from_others_in_postcode(self):
        others = (
            Address.objects.filter(postcode=self.postcode)
            .exclude(uprntocouncil__isnull=True)
            .distinct("uprntocouncil__lad")
        )
        if len(others) == 1:
            return others[0].council
        else:
            return None

    @property
    def council_id(self):
        return self.council.council_id

    @property
    def council(self):
        return Council.objects.get(geography__gss=self.uprntocouncil.lad)

    @property
    def polling_station_id(self):
        return self.uprntocouncil.polling_station_id

    @property
    def polling_station(self):
        station = PollingStation.objects.filter(
            internal_council_id=self.polling_station_id, council_id=self.council_id
        )
        if len(station) == 1:
            return station[0]
        else:
            return None


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


def get_uprn_hash_table(gss_code):
    addresses = Address.objects.filter(uprntocouncil__lad=gss_code)
    # return result a hash table keyed by UPRN
    return {
        a.uprn: {
            "address": a.address,
            "postcode": a.postcode.replace(" ", ""),
            "location": a.location,
        }
        for a in addresses
    }
