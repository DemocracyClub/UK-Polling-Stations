from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WEW"
    addresses_name = "2024-07-04/2024-06-24T13:51:35.135872/WEW_combined.csv"
    stations_name = "2024-07-04/2024-06-24T13:51:35.135872/WEW_combined.csv"
    elections = ["2024-07-04"]

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
