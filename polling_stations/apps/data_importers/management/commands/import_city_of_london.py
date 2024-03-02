from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "LND"
    addresses_name = "2024-05-02/2024-03-02T12:50:38.332841/Democracy Club - Polling Districts GLA.csv"
    stations_name = "2024-05-02/2024-03-02T12:50:38.332841/Democracy Club - Polling Stations GLA.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # "St Bride Foundation Institute"
        if record.stationcode == "SBF":
            record = record._replace(xordinate="531586")
            record = record._replace(yordinate="181081")
        # "St Giles' Cripplegate"
        if record.stationcode == "SGC1":
            record = record._replace(xordinate="532350")
            record = record._replace(yordinate="181702")
        # "St Giles' Cripplegate"
        if record.stationcode == "SGC2":
            record = record._replace(xordinate="532350")
            record = record._replace(yordinate="181702")

        return super().station_record_to_dict(record)
