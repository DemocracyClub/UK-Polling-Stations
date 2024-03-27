from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEA"
    addresses_name = "2024-05-02/2024-03-27T14:37:19.282513/Eros_SQL_Output004.csv"
    stations_name = "2024-05-02/2024-03-27T14:37:19.282513/Eros_SQL_Output004.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "NG24 4JW",
            "NG24 4BT",
            "NG24 3PA",
            "NG25 0LQ",
            "NG24 5BS",
            "NG21 9EE",
        ]:
            return None
        return super().address_record_to_dict(record)
