from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WAT"
    addresses_name = (
        "2024-07-04/2024-06-05T15:48:24.091486/Watford Democracy Counts Extract.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-05T15:48:24.091486/Watford Democracy Counts Extract.csv"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # splits
            "WD25 9AS",
            "WD18 7BS",
            "WD25 7DA",
        ]:
            return None

        return super().address_record_to_dict(record)
