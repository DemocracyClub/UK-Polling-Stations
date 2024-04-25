from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "BAS"
    addresses_name = "2024-05-02/2024-03-15T16:30:23.414487/Bath&NESomerset.csv"
    stations_name = "2024-05-02/2024-03-15T16:30:23.414487/Bath&NESomerset.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10094952037",  # KINGSHILL FARM, BRISTOL ROAD, COMPTON MARTIN, BRISTOL
            "100120029109",  # 15 UPPER BLOOMFIELD ROAD, BATH
            "10093714965",  # THE STABLE, GIBBET LANE, BRISTOL
        ]:
            return None

        if record.housepostcode in [
            # split
            "BA2 6DR",
            "BA2 5AD",
            "BA2 2RZ",
            # suspect
            "BA3 5SF",
        ]:
            return None
        return super().address_record_to_dict(record)

    def get_station_point(self, record):
        uprn = record.pollingvenueuprn.strip().lstrip("0")
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except ObjectDoesNotExist:
            return super().get_station_point(record)

    def station_record_to_dict(self, record):
        # Weston Free Church, High Street, Upper Weston, Bath BA1 4DB
        if self.get_station_hash(record) in (
            "144-weston-free-church",
            "145-weston-free-church",
        ):
            record = record._replace(pollingvenueuprn="10001147059")

        return super().station_record_to_dict(record)
