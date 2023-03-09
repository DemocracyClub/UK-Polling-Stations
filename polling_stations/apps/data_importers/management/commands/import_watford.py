from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WAT"
    addresses_name = "2023-05-04/2023-03-09T16:41:25.854790/Eros_SQL_Output071.csv"
    stations_name = "2023-05-04/2023-03-09T16:41:25.854790/Eros_SQL_Output071.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "WD25 9AS",
            "WD25 7DA",
            "WD18 7BS",
        ]:
            return None
        return super().address_record_to_dict(record)
