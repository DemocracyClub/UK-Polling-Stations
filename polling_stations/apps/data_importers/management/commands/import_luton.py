from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "LUT"
    addresses_name = (
        "2024-07-04/2024-05-28T16:47:53.627930/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T16:47:53.627930/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100080141870",  # 169 DEWSBURY ROAD, LUTON
            "100080163617",  # 117 NEVILLE ROAD, LUTON
            "100080124758",  # 166 ALEXANDRA AVENUE, LUTON
            "10095334110",  # 654A DENBIGH ROAD, LUTON
        ]:
            return None

        if record.postcode in [
            # splits
            "LU1 3XD",
            # looks wrong
            "LU2 8PE",
        ]:
            return None

        return super().address_record_to_dict(record)
