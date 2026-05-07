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

    def station_record_to_dict(self, record):
        # bug report: https://app.asana.com/1/1204880536137786/project/1207538772343223/task/1214601728656227?focus=true
        # Fix coords for:
        # THE LEARNING CENTRE, 81 ALEXANDER ROAD, GLENROTHES, KY7 4EF
        if record.stationcode in [
            "185",
            "186",
        ]:
            record = record._replace(
                polling_place_easting="327592",
                polling_place_northing="700592",
            )
        return super().station_record_to_dict(record)

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
