from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RUT"
    addresses_name = "2024-07-04/2024-06-27T13:23:00.744586/Eros_SQL_Output002.csv"
    stations_name = "2024-07-04/2024-06-27T13:23:00.744586/Eros_SQL_Output002.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "PE9 3SR",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
