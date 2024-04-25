from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "TOF"
    addresses_name = (
        "2024-05-02/2024-03-08T13:10:09.629993/Export From Query for Caroline v4.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-08T13:10:09.629993/Export From Query for Caroline v4.csv"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002953910",  # PARK HOUSE FARM, GRAIG ROAD, UPPER CWMBRAN, CWMBRAN
        ]:
            return None

        if record.housepostcode.strip() in [
            # split
            "NP4 8LG",
            "NP4 7NW",
            "NP44 5AB",
            # suspect
            "NP4 8QW",
            "NP4 8QP",
            "NP4 6TX",
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
