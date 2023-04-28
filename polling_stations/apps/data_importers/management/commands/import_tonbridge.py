from data_importers.ems_importers import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TON"
    addresses_name = "2023-05-04/2023-04-28T13:21:46.272897/Eros_SQL_Output001.csv"
    stations_name = "2023-05-04/2023-04-28T13:21:46.272897/Eros_SQL_Output001.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "TN11 0ES",
            "ME19 5PA",
            "ME19 5LL",
            "TN10 4JJ",
            "TN11 0AJ",
        ]:
            return None
        return super().address_record_to_dict(record)
