from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = (
        "2026-07-16/2026-06-24T16:41:41.653558/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2026-07-16/2026-06-24T16:41:41.653558/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-07-16"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # The folowing are station coord corrections supplied by council:

        # WEST EARLHAM COMMUNITY CENTRE, 10 WILBERFORCE ROAD, NORWICH, NR5 8ND
        if record.stationcode == "48UN5":
            record = record._replace(
                xordinate="619054",
                yordinate="308709",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "NR3 2LE",
            # looks wrong
            "NR5 8NA",
        ]:
            return None

        return super().address_record_to_dict(record)
