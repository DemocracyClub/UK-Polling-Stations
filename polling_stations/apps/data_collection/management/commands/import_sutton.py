from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E09000029"
    addresses_name = (
        "local.2018-05-03/Version 2/Democracy Club - Polling Districts Sutton.csv"
    )
    stations_name = (
        "local.2018-05-03/Version 2/Democracy Club - Polling Stations Sutton.csv"
    )
    elections = ["local.2018-05-03"]

    def address_record_to_dict(self, record):
        if record.uprn == "5870022328":
            rec = super().address_record_to_dict(record)
            rec["polling_station_id"] = ""
            return rec
        return super().address_record_to_dict(record)
