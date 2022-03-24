from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WKF"
    addresses_name = "2022-05-05/2022-03-24T08:44:15.467165/Democracy Club - Polling Districts - May 2022 Elections Wakefield.csv"
    stations_name = "2022-05-05/2022-03-24T08:44:15.467165/Democracy Club - Polling Stations - May 2022 Elections Wakefield.csv"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.uprn in [
            "63111468",
            "63194364",
            "63192244",
            "63185795",
            "63192242",
            "63065258",
            "63194974",
        ]:
            return None
        if record.postcode.strip() in [
            "WF5 0RT",
            "WF2 6JA",
            "WF2 0RG",
            "WF1 4GA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # THREE LANE ENDS ACADEMY
        if record.stationcode == "22-03NG":
            record = record._replace(xordinate="", yordinate="")
        return super().station_record_to_dict(record)
