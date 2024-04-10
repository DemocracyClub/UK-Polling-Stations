from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "WEW"
    addresses_name = "2024-05-02/2024-04-10T08:57:27.773069/Eros_SQL_Output003.csv"
    stations_name = "2024-05-02/2024-04-10T08:57:27.773069/Eros_SQL_Output003.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100081149200",  # SANDYHURST, WELWYN BY PASS ROAD, WELWYN
            "10091064276",  # FLAT 1, 199 ST. ALBANS ROAD WEST, HATFIELD AL10 0SZ
            "10091064277",  # FLAT 2, 199 ST. ALBANS ROAD WEST, HATFIELD AL10 0SZ
            "10091064278",  # FLAT 3, 199 ST. ALBANS ROAD WEST, HATFIELD AL10 0SZ
            "10091064279",  # FLAT 4, 199 ST. ALBANS ROAD WEST, HATFIELD AL10 0SZ
            "10091064280",  # FLAT 5, 199 ST. ALBANS ROAD WEST, HATFIELD AL10 0SZ
            "10091064281",  # FLAT 6, 199 ST. ALBANS ROAD WEST, HATFIELD AL10 0SZ
            "10091064282",  # FLAT 7, 199 ST. ALBANS ROAD WEST, HATFIELD AL10 0SZ
            "10091064283",  # FLAT 8, 199 ST. ALBANS ROAD WEST, HATFIELD AL10 0SZ
            "10091064284",  # FLAT 9, 199 ST. ALBANS ROAD WEST, HATFIELD AL10 0SZ
            "200003853601",  # THE PRESBYTERY, ST. PETERS RC CHURCH, BISHOPS RISE, HATFIELD
        ]:
            return None

        if record.housepostcode in [
            # suspect
            "AL6 9FJ",  # WELWYN BY PASS ROAD, WELWYN
            "AL6 9AF",  # WHITEHILL, WELWYN
            "AL10 0TA",  # ST. ALBANS ROAD WEST, HATFIELD
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
