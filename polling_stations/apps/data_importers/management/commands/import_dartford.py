from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "DAR"
    addresses_name = "2024-05-02/2024-03-08T15:19:40.671473/Eros_SQL_Output002.csv"
    stations_name = "2024-05-02/2024-03-08T15:19:40.671473/Eros_SQL_Output002.csv"
    elections = ["2024-05-02"]

    # quick fix to show maps for Halarose records that have a valid UPRN in the PollingVenueUPRN field
    def get_station_point(self, record):
        uprn = record.pollingvenueuprn.strip().lstrip("0")
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except ObjectDoesNotExist:
            return super().get_station_point(record)

    def station_record_to_dict(self, record):
        # UPRN update from council:
        # Greenhithe Masonic Lodge, 218 London Road, Greenhithe, Dartford DA9 9JF
        if self.get_station_hash(record) == "43-greenhithe-masonic-lodge":
            record = record._replace(pollingvenueuprn="200000534103")

        return super().station_record_to_dict(record)
