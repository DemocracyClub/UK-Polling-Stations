from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ZET"
    addresses_name = "2021-03-23T15:04:56.746808/polling_station_export-2021-03-19.csv"
    stations_name = "2021-03-23T15:04:56.746808/polling_station_export-2021-03-19.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "30100007505",  # NORTH BOOTH, HAROLDSWICK, UNST, SHETLAND
            "30100000940",  # HOUSE A B9088 FROM HERRA X-ROADS TO BAELA JUNCTION, HOUBIE, FETLAR
        ]:
            return None

        if record.housepostcode in ["ZE2 9HD"]:
            return None

        return super().address_record_to_dict(record)
