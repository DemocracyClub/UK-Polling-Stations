from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ZET"
    addresses_name = (
        "2024-07-04/2024-06-20T14:57:44.630295/Shetland Eros_SQL_Output004.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-20T14:57:44.630295/Shetland Eros_SQL_Output004.csv"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "30100007505",  # NORTH BOOTH, HAROLDSWICK, UNST, SHETLAND
            "30100005132",  # BOOTH, OLLABERRY, SHETLAND
        ]:
            return None

        return super().address_record_to_dict(record)
