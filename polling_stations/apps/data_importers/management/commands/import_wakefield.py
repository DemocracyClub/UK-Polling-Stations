from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WKF"
    addresses_name = "2026-05-07/2026-04-21T10:23:04.009045/20260421 Demo Club PDs.csv"
    stations_name = (
        "2026-05-07/2026-04-21T10:23:04.009045/20260421 Demo Club Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode.strip() in [
            # splits
            "WF5 0NR",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # WARNING: Polling station ST PAULS METHODIST CHURCH, Chapel Street, Ryhill, WF4 2AD is in Bradford Council
        # Address correct, removed wrong coords
        if record.stationcode == "039":
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)
