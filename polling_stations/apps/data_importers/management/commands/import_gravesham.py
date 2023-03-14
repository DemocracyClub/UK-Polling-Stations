from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GRA"
    addresses_name = "2023-05-04/2023-02-21T21:14:28.593307/polling-stations-export.csv"
    stations_name = "2023-05-04/2023-02-21T21:14:28.593307/polling-stations-export.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in ["ME3 7NB"]:
            return None

        return super().address_record_to_dict(record)
