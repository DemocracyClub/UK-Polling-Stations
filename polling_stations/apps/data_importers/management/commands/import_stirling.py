from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "STG"
    addresses_name = "2024-07-04/2024-06-04T16:53:58.873569/Eros_SQL_Output009.csv"
    stations_name = "2024-07-04/2024-06-04T16:53:58.873569/Eros_SQL_Output009.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "FK8 1TX",
            "G63 9HS",
            "FK7 0LS",
        ]:
            return None
        return super().address_record_to_dict(record)
