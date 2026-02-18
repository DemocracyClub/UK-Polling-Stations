from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FIF"
    addresses_name = (
        "2026-05-07/2026-02-18T15:06:41.753682/Democracy Club - Polling District 2.csv"
    )
    stations_name = (
        "2026-05-07/2026-02-18T15:06:41.753682/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "320232414",  # 8 VIEWFIELD TERRACE, DUNFERMLINE, KY12 7HZ
            "320329489",  # 34 RITCHIE AVENUE, DUNFERMLINE
            "320329487",  # 32 RITCHIE AVENUE, DUNFERMLINE
        ]:
            return None

        if record.postcode in [
            # split
            "KY12 8DT",
            "KY8 2EZ",
            "KY3 0RW",
            # looks wrong
            "KY12 9GP",
            "KY4 8ES",
        ]:
            return None

        return super().address_record_to_dict(record)
