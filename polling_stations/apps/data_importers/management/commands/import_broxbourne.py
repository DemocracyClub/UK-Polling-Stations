from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRX"
    addresses_name = "2025-05-01/2025-03-24T16:55:00.760095/Democracy Club - polling districts for 1-5-2025.csv"
    stations_name = "2025-05-01/2025-03-24T16:55:00.760095/Democracy Club - polling stations for 1-5-2025.csv"
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
