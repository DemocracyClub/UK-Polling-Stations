from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "SSO"
    addresses_name = "2024-05-02/2024-02-29T14:44:57.333133/Eros_SQL_Output002 (1).csv"
    stations_name = "2024-05-02/2024-02-29T14:44:57.333133/Eros_SQL_Output002 (1).csv"
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # OAKLANDS PRIMARY SCHOOL, PRESTON GROVE, YEOVIL BA20 2DY
        if (record.pollingstationnumber, record.pollingstationname) == (
            "79",
            "OAKLANDS PRIMARY SCHOOL",
        ):
            record = record._replace(pollingstationpostcode="BA20 2DU")
        # MARTOCK UNITED REFORMED CHURCH HALL, BOWER HINTON, MARTOCK, SOMERSET TA12 6JN
        if (record.pollingstationnumber, record.pollingstationname) == (
            "93",
            "MARTOCK UNITED REFORMED CHURCH HALL",
        ):
            record = record._replace(pollingstationpostcode="TA12 6LA")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "TA20 2NJ",
            "BA10 0BU",
            "BA9 9NZ",
            "TA20 2BE",
            "TA10 0HF",
            "BA22 8NT",
            "TA3 6RP",
            "TA10 0PJ",
            "TA10 0QH",
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
