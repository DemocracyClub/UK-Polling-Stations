from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E09000021"
    stations_name = "europarl.2019-05-23/Version 1/Democracy Club - Polling Stations - 23 May 2019.csv"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy Club - Polling Districts - 23 May 2019.csv"
    elections = ["europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        if record.postcode == "KT1 1HG":
            return None
        return super().address_record_to_dict(record)
