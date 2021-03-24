from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BAR"
    addresses_name = "2021-03-08T19:54:15.110811/Barrow in Furness Democracy Club - Polling Districts (2).csv"
    stations_name = "2021-03-08T19:54:15.110811/Barrow in Furness Democracy Club - Polling Stations (2).csv"
    elections = ["2021-05-06"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        if record.postcode in ["LA13 9SF", "LA13 0NF"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # ASKAM COMMUNITY CENTRE
        if record.stationcode in ["LC/1", "LC/2"]:
            record = record._replace(xordinate="321435")
            record = record._replace(yordinate="477563")

        # VICKERSTOWN METHODIST CHURCH
        if record.stationcode == "AA/1":
            record = record._replace(xordinate="318614")
            record = record._replace(yordinate="468960")

        return super().station_record_to_dict(record)
