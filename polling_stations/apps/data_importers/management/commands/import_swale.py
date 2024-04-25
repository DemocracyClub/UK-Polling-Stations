from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "SWL"
    addresses_name = (
        "2024-05-02/2024-03-22T14:00:13.485984/SWALE_Eros_SQL_Output001.csv"
    )
    stations_name = "2024-05-02/2024-03-22T14:00:13.485984/SWALE_Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if record.housepostcode in [
            # split
            "ME10 2EF",
            "ME12 2SG",
            "ME12 1TF",
            "ME10 3TU",
            # suspect
            "ME12 1RW",
            "ME12 1RN",
        ]:
            return None

        if uprn in [
            "200002533735",  # POPPINGTON BUNGALOW, WHITE HILL, SELLING, FAVERSHAM
            "100061091546",  # 31 HAMBROOK WALK, SITTINGBOURNE
            "100061091542",  # 27 HAMBROOK WALK, SITTINGBOURNE
            "100061091544",  # 29 HAMBROOK WALK, SITTINGBOURNE
            "100061091540",  # 25 HAMBROOK WALK, SITTINGBOURNE
            "10093084893",  # 3 HOUSSON AVENUE, SITTINGBOURNE
            "10093084895",  # 5 HOUSSON AVENUE, SITTINGBOURNE
            "10093084891",  # 1 HOUSSON AVENUE, SITTINGBOURNE
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
