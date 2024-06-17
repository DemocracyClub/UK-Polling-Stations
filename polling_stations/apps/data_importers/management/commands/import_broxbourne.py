from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRX"
    addresses_name = "2024-07-04/2024-06-17T12:51:05.354706/Democracy Club -  Poling Districts for Borough of Broxbourne for 4-7-2024.csv"
    stations_name = "2024-07-04/2024-06-17T12:51:05.354706/Democracy Club - Polling stations for Borough of Broxbourne for 4-7-2024.csv"
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip("0").strip()

        if uprn in [
            "148043016",  # 11 ABINGDON COURT, HIGH STREET, WALTHAM CROSS
            "148046333",  # KIMBLE, HIGHFIELD STABLES, WHITE STUBBS LANE, BROXBOURNE
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Remove stations from EHE council
        if record.stationcode in ["29", "30", "31", "32", "33", "34"]:
            return None

        return super().station_record_to_dict(record)
