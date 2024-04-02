from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "TON"
    addresses_name = "2024-05-02/2024-04-02T15:35:52.601856/Eros_SQL_Output002.csv"
    stations_name = "2024-05-02/2024-04-02T15:35:52.601856/Eros_SQL_Output002.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "TN11 0AJ",
            "TN10 4JJ",
            "TN11 0ES",
            "ME20 6HZ",
            "ME19 5PA",
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
