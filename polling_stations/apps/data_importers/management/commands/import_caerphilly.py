from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "CAY"
    addresses_name = "2024-05-02/2024-03-22T14:36:48.765501/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-22T14:36:48.765501/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "43171669",  # THE LODGE, STABLES COMPOUND, WEST ROAD, PENALLTA INDUSTRIAL ESTATE, PENALLTA, HENGOED
        ]:
            return None
        if record.housepostcode in [
            "NP11 6JE",
            "CF83 8RL",
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
