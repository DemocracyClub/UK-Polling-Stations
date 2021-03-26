from data_importers.ems_importers import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "LND"
    addresses_name = "2021-03-24T11:43:05.269487146/Polling Districts - CoL.csv"
    stations_name = "2021-03-24T11:43:05.269487146/Polling Stations - CoL.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        # "St Bride Foundation Institute"
        if record.stationcode == "AL":
            record = record._replace(xordinate="531586")
            record = record._replace(yordinate="181081")
        # "St Giles' Cripplegate"
        if record.stationcode == "BL_1":
            record = record._replace(xordinate="532350")
            record = record._replace(yordinate="181702")
        # "St Giles' Cripplegate"
        if record.stationcode == "BL_2":
            record = record._replace(xordinate="532350")
            record = record._replace(yordinate="181702")

        return super().station_record_to_dict(record)
