from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RUT"
    addresses_name = "2024-05-02/2024-02-28T09:23:18.188114/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-02-28T09:23:18.188114/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "PE9 3SR",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
