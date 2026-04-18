from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "WEW"
    addresses_name = "2026-05-07/2026-04-17T15:42:56.274280/Democracy Club - Idox_2026-04-17 15-31.csv"
    stations_name = "2026-05-07/2026-04-17T15:42:56.274280/Democracy Club - Idox_2026-04-17 15-31.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "100081149200",  # SANDYHURST, WELWYN BY PASS ROAD, WELWYN
                "200003853601",  # THE PRESBYTERY, ST. PETERS RC CHURCH, BISHOPS RISE, HATFIELD
            ]
        ):
            return None

        if record.postcode in [
            # suspect
            "AL6 9FJ",
            "AL6 9AF",
            "AL10 0TA",
            "AL10 0SZ",
            "AL7 2FB",
        ]:
            return None
        return super().address_record_to_dict(record)
