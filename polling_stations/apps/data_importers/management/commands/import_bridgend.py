from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "BGE"
    addresses_name = "2024-05-02/2024-03-28T16:34:21.170746/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-28T16:34:21.170746/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "CF34 0UF",
            "CF32 8TY",
            "CF31 2DH",
            "CF31 5FD",
            "CF31 3HL",
            "CF31 1NP",
            "CF34 9SD",
            "CF35 6GD",
            "CF33 6PL",
            "CF35 6HZ",
            "CF32 0NR",
            # suspect
            "CF31 2DL",  #
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
