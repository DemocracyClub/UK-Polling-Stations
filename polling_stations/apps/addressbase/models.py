from django.contrib.gis.db import models
from uk_geo_utils.models import (
    AbstractAddress,
    AbstractOnsudManager,
)

from councils.models import Council
from pollingstations.models import PollingStation


class Address(AbstractAddress):
    @property
    def council_id(self):
        return self.uprntocouncil.lad

    @property
    def council(self):
        return Council.objects.get(council_id=self.council_id)

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
