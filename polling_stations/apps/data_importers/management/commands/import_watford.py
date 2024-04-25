from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "WAT"
    addresses_name = (
        "2024-05-02/2024-02-22T15:03:32.581902/Watford BC Democracy Club Data.csv"
    )
    stations_name = (
        "2024-05-02/2024-02-22T15:03:32.581902/Watford BC Democracy Club Data.csv"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "WD25 9AS",
            "WD18 7BS",
            "WD25 7DA",
        ]:
            return None

        return super().address_record_to_dict(record)

    # quick fix to show maps for Halarose records that have a valid UPRN in the PollingVenueUPRN field
    def get_station_point(self, record):
        uprn = record.pollingvenueuprn.strip().lstrip("0")
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except ObjectDoesNotExist:
            return super().get_station_point(record)
