from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRX"
    addresses_name = "2024-05-02/2024-02-28T15:22:27.029172/Democracy Club - Polling Districts for 2-5-2024.csv"
    stations_name = "2024-05-02/2024-02-28T15:22:27.029172/Democracy Club - Polling Stations for 2-5-2024.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip("0").strip()

        if uprn in [
            "148043016",  # 11 ABINGDON COURT, HIGH STREET, WALTHAM CROSS
            "148046333",  # KIMBLE, HIGHFIELD STABLES, WHITE STUBBS LANE, BROXBOURNE
        ]:
            return None

        return super().address_record_to_dict(record)
