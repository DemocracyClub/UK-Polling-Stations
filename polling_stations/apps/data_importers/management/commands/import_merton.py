from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MRT"
    addresses_name = (
        "2021-04-16T12:08:03.317001/polling_station_export-2021-04-15 Merton.csv"
    )
    stations_name = (
        "2021-04-16T12:08:03.317001/polling_station_export-2021-04-15 Merton.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "48108063",  # HOUSE 159 COMMONSIDE EAST, MITCHAM
        ]:
            return None

        if record.housepostcode in ["KT3 6LZ", "SW19 2FJ", "SM4 6BE", "SM4 6BB"]:
            return None

        return super().address_record_to_dict(record)
