from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EAS"
    addresses_name = "2023-05-04/2023-03-08T12:16:19.775860/Eros_SQL_Output001.csv"
    stations_name = "2023-05-04/2023-03-08T12:16:19.775860/Eros_SQL_Output001.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode in [
            "BN20 7AU",
            "BN23 8JH",  # split
        ]:
            return None

        if uprn in [
            "10010662297",  # 10010662297
        ]:
            return None

        return super().address_record_to_dict(record)
