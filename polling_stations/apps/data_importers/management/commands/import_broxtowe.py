from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BRT"
    addresses_name = "2024-07-04/2024-05-30T14:47:06.249789/Eros_SQL_Output002.csv"
    stations_name = "2024-07-04/2024-05-30T14:47:06.249789/Eros_SQL_Output002.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10013966545",  # 14A TRENT ROAD, BEESTON, NOTTINGHAM
            "10013966491",  # 34 TRENT ROAD, BEESTON, NOTTINGHAM
            "10003431083",  # 5A TRENT ROAD, BEESTON, NOTTINGHAM
            "10013964473",  # 44A MEADOW ROAD, BEESTON, NOTTINGHAM
        ]:
            return None

        return super().address_record_to_dict(record)
