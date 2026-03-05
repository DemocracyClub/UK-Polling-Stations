from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WKF"
    addresses_name = "2026-05-07/2026-03-05T11:29:56.194818/20260305 Democracy Club Polling Districts.csv"
    stations_name = "2026-05-07/2026-03-05T11:29:56.194818/20260305 Democracy Club Polling Stations.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16-le"

    # workaround for files having different encodings
    def get_stations(self):
        self.csv_encoding = "utf-8"
        stations = super().get_stations()
        self.csv_encoding = "utf-16-le"
        return stations

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
