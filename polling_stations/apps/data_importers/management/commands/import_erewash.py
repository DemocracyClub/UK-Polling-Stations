from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ERE"
    addresses_name = "2023-05-04/2023-03-30T15:20:26.308217/Eros_SQL_Output001.csv"
    stations_name = "2023-05-04/2023-03-30T15:20:26.308217/Eros_SQL_Output001.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in []:
            return None

        if record.housepostcode in [
            # split
            "DE7 8TB",
            "NG10 4BH",
        ]:
            return None

        return super().address_record_to_dict(record)
