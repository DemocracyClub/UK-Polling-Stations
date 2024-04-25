from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "NEL"
    addresses_name = "2024-05-02/2024-03-12T11:47:38.056186/Eros_SQL_Output004.csv"
    stations_name = "2024-05-02/2024-03-12T11:47:38.056186/Eros_SQL_Output004.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090078903",  # FLAT, 247 GRIMSBY ROAD, CLEETHORPES
            "10090086605",  # THE ROOST, DIANA PRINCESS OF WALES HOSPITAL, SCARTHO ROAD, GRIMSBY
            "10090078890",  # FLAT 3, 50 RUTLAND STREET, GRIMSBY
            "10090078888",  # FLAT 1, 50 RUTLAND STREET, GRIMSBY
            "10090078889",  # FLAT 2, 50 RUTLAND STREET, GRIMSBY
            "10090078891",  # FLAT 4, 50 RUTLAND STREET, GRIMSBY
            "11023550",  # 38 BRAMHALL STREET, CLEETHORPES
            "11088787",  # 4 WALTHAM HOUSE FARM COTTAGE, LOUTH ROAD, NEW WALTHAM, GRIMSBY
            "11088786",  # WALTHAM HOUSE FARM COTTAGE 3 LOUTH ROAD, WALTHAM
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
