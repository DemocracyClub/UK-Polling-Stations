from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "RCT"
    addresses_name = "2024-07-04/2024-05-30T10:52:42.568781/Eros_SQL_Output006.csv"
    stations_name = "2024-07-04/2024-05-30T10:52:42.568781/Eros_SQL_Output006.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # postcode correction for: ST DAVIDS CHURCH, LLANTRISANT ROAD, GROESFAEN, PONTYCLUN, CF72 8NU
        # there are 2 stations with the same pollingstationnumber, hence extra condition
        if (
            record.pollingstationnumber == "58"
            and "ST DAVIDS CHURCH" in record.pollingstationname
        ):
            record = record._replace(pollingstationpostcode="CF72 8NS")

        return super().station_record_to_dict(record)

    # quick fix to show maps for Halarose records that have a valid UPRN in the PollingVenueUPRN field
    def get_station_point(self, record):
        uprn = record.pollingvenueuprn.strip().lstrip("0")
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except ObjectDoesNotExist:
            return super().get_station_point(record)
