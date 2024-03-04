from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "LUT"
    addresses_name = (
        "2024-05-02/2024-02-27T18:23:10.452598/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-02-27T18:23:10.452598/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100080141870",  # 169 DEWSBURY ROAD, LUTON
            "100080163617",  # 117 NEVILLE ROAD, LUTON
            "100080124758",  # 166 ALEXANDRA AVENUE, LUTON
        ]:
            return None

        if record.postcode in [
            # looks wrong
            "LU2 8PE"
        ]:
            return None

        return super().address_record_to_dict(record)
