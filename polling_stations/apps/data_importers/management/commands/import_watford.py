from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WAT"
    addresses_name = (
        "2024-05-02/2024-02-22T15:03:32.581902/Watford BC Democracy Club Data.csv"
    )
    stations_name = (
        "2024-05-02/2024-02-22T15:03:32.581902/Watford BC Democracy Club Data.csv"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "WD25 9AS",
            "WD18 7BS",
            "WD25 7DA",
        ]:
            return None

        return super().address_record_to_dict(record)
