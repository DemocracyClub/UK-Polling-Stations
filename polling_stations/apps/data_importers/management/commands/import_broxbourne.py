from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRX"
    addresses_name = "2025-05-01/2025-03-18T15:21:50.978077/DC - Polling Districts.csv"
    stations_name = "2025-05-01/2025-03-18T15:21:50.978077/DC - Polling Stations.csv"
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip("0").strip()

        if uprn in [
            "148043016",  # 11 ABINGDON COURT, HIGH STREET, WALTHAM CROSS
            "148046333",  # KIMBLE, HIGHFIELD STABLES, WHITE STUBBS LANE, BROXBOURNE
        ]:
            return None

        return super().address_record_to_dict(record)
