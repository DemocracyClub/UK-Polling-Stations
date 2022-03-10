from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ZET"
    addresses_name = (
        "2022-05-05/2022-03-10T14:33:34.834669/polling_station_export-2022-03-10.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-10T14:33:34.834669/polling_station_export-2022-03-10.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "30100007505",  # NORTH BOOTH, HAROLDSWICK, UNST, SHETLAND
            "30100005132",  # BOOTH, OLLABERRY, SHETLAND
        ]:
            return None

        if record.housepostcode in [
            "ZE1 0UX",
            "ZE2 9HD",
        ]:
            return None

        return super().address_record_to_dict(record)
