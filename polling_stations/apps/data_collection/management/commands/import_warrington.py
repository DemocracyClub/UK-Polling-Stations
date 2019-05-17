from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E06000007"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy Club - Polling districts Warrington.csv"
    stations_name = (
        "europarl.2019-05-23/Version 1/Democracy Club - Polling Stations Warrington.csv"
    )
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):

        # Westbrook Old Hall Primary School
        if record.stationcode in ["12X", "77"]:
            record = record._replace(postcode="WA5 9QA")

        return super().station_record_to_dict(record)
