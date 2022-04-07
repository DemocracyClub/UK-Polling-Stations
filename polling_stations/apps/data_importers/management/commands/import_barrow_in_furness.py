from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BAR"
    addresses_name = (
        "2022-05-05/2022-04-07T14:47:44.793330/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-07T14:47:44.793330/Democracy Club - polling stations.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # ASKAM COMMUNITY CENTRE
        if record.stationcode in ["LC1", "LC2"]:
            record = record._replace(xordinate="321435")
            record = record._replace(yordinate="477563")

        # VICKERSTOWN METHODIST CHURCH
        if record.stationcode == "AA1":
            record = record._replace(xordinate="318614")
            record = record._replace(yordinate="468960")

        return super().station_record_to_dict(record)
