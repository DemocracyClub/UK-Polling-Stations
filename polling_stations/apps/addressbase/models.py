from councils.models import Council
from data_importers.event_types import DataEventType
from data_importers.models import DataEvent
from django.contrib.gis.db import models
from django.contrib.postgres.indexes import BTreeIndex, GistIndex
from django.db.models import OuterRef, Subquery
from pollingstations.models import PollingStation, VisibilityChoices
from uk_geo_utils.models import (
    AbstractAddress,
    AbstractOnsudManager,
)


class Address(AbstractAddress):
    class Meta:
        indexes = [
            BTreeIndex(
                fields=["uprn"],
                name="address_uprn_like_idx",
                opclasses=["varchar_pattern_ops"],
            ),
            BTreeIndex(fields=["postcode"], name="address_postcode_idx"),
            BTreeIndex(
                fields=["postcode"],
                name="address_postcode_like_idx",
                opclasses=["varchar_pattern_ops"],
            ),
            GistIndex(fields=["location"], name="address_location_gist"),
        ]

    def get_council_from_others_in_postcode(self):
        others = (
            Address.objects.filter(postcode=self.postcode)
            .exclude(uprntocouncil__isnull=True)
            .distinct("uprntocouncil__lad")
        )
        if len(others) == 1:
            return others[0].council

        return None

    @property
    def council_id(self):
        return self.council.council_id

    @property
    def council(self):
        return Council.objects.get(geography__gss=self.uprntocouncil.lad)

    @property
    def council_name(self):
        if not hasattr(self, "_council_name"):
            self._council_name = self.council.name
        return self._council_name

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
        return None

    def polling_station_with_elections(self, include_unpublished=False):
        """
        Returns the polling station for this address,
        with the elections field from the most recent data import event
        for the relevant council
        """
        visibilities = [VisibilityChoices.PUBLISHED]
        if include_unpublished:
            visibilities.append(VisibilityChoices.UNPUBLISHED)
        try:
            elections = Subquery(
                DataEvent.objects.filter(
                    council_id=OuterRef("council_id"), event_type=DataEventType.IMPORT
                )
                .order_by("-created")
                .values("election_dates")[:1]
            )
            return (
                PollingStation.objects.annotate(elections=elections)
                .select_related("accessibility_information")
                .get(
                    internal_council_id=self.polling_station_id,
                    council_id=self.council_id,
                    visibility__in=visibilities,
                )
            )
        except PollingStation.DoesNotExist:
            return None
        except DataEvent.DoesNotExist:
            return None


class UprnToCouncil(models.Model):
    class Meta:
        indexes = [
            BTreeIndex(fields=["lad"], name="uprntocouncil_lad_idx"),
            BTreeIndex(
                fields=["uprn"],
                name="uprntocouncil_uprn_like_idx",
                opclasses=["varchar_pattern_ops"],
            ),
            BTreeIndex(
                fields=["advance_voting_station"],
                name="uprntocouncil_adv_v_station_idx",
            ),
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
    advance_voting_station = models.ForeignKey(
        "pollingstations.AdvanceVotingStation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


def get_uprn_hash_table(gss_codes: list[str]) -> dict[str, dict[str:str]]:
    """
    Takes a list of gss codes and returns a dict with shape:
    {
        <uprn>: {
            "address": <address>,
            "postcode": <postcode>,
            "location": <location>
        }
    }
    """
    addresses = Address.objects.filter(uprntocouncil__lad__in=gss_codes)
    # return result a hash table keyed by UPRN
    return {
        a.uprn: {
            "address": a.address,
            "postcode": a.postcode.replace(" ", ""),
            "location": a.location,
        }
        for a in addresses
    }
