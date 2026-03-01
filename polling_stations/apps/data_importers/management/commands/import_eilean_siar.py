from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ELS"
    addresses_name = "2026-05-07/2026-03-01T07:46:42.121381/Democracy Club - Polling Districts WI.csv"
    stations_name = (
        "2026-05-07/2026-03-01T07:46:42.121381/Democracy Club - Polling Stations WI.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.uprn in [
            "139014479",  # 5 SEAFORTH HEAD, ISLE OF LEWIS, HS2 9LG
        ]:
            return None

        if record.postcode in [
            # looks wrong
            "HS3 3AE",
        ]:
            return None

        return super().address_record_to_dict(record)
