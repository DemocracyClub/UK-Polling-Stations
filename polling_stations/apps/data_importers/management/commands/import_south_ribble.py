from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "SRI"
    addresses_name = "2024-05-02/2024-03-19T15:12:00.400914/Eros_SQL_Output004.csv"
    stations_name = "2024-05-02/2024-03-19T15:12:00.400914/Eros_SQL_Output004.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "PR5 5AU",  # split
        ]:
            return None

        if record.uprn in [
            "100010637839",  # 73A LIVERPOOL OLD ROAD, WALMER BRIDGE, PRESTON
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
