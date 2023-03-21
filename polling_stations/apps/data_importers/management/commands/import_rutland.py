from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RUT"
    addresses_name = "2023-05-04/2023-03-21T11:42:59.411435/Eros_SQL_Output002.csv"
    stations_name = "2023-05-04/2023-03-21T11:42:59.411435/Eros_SQL_Output002.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in ["PE9 3SR"]:
            return None  # split

        return super().address_record_to_dict(record)
