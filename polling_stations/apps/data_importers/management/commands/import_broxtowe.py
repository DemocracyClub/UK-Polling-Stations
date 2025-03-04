from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BRT"
    addresses_name = "2025-05-01/2025-03-04T15:02:27.653222/Eros_SQL_Output003.csv"
    stations_name = "2025-05-01/2025-03-04T15:02:27.653222/Eros_SQL_Output003.csv"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10013966545",  # 14A TRENT ROAD, BEESTON, NOTTINGHAM
            "10013966491",  # 34 TRENT ROAD, BEESTON, NOTTINGHAM
            "10003431083",  # 5A TRENT ROAD, BEESTON, NOTTINGHAM
            "10013964473",  # 44A MEADOW ROAD, BEESTON, NOTTINGHAM
            "100031336319",  # 37 SCARGILL AVENUE, NEWTHORPE, NOTTINGHAM
        ]:
            return None

        return super().address_record_to_dict(record)
