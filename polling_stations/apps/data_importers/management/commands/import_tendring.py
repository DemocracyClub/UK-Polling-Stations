from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "TEN"
    addresses_name = (
        "2026-08-13/2026-07-24T09:33:34.314482/Pollin Station Districts UKPBE.csv"
    )
    stations_name = "2026-08-13/2026-07-24T09:33:34.314482/DC Polling Staions UKPBE.csv"
    elections = ["2026-08-13"]
    csv_encoding = "utf-16le"
