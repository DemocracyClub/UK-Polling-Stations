from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E09000021"
    addresses_name = (
        "local.2018-05-03/Version 2/Democracy Club - Polling Districts Kingston.csv"
    )
    stations_name = (
        "local.2018-05-03/Version 3/Kingston Borough 2018 - Polling Stations.csv"
    )
    elections = ["local.2018-05-03"]

    def address_record_to_dict(self, record):

        if record.postcode == "KT1 3JU":
            return None
        if record.postcode == "KT1 1HG":
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        if record.stationcode in ["MB_65", "MB_66"]:
            record = record._replace(xordinate="518811")
            record = record._replace(yordinate="166015")

        return super().station_record_to_dict(record)
