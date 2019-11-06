from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E09000021"
    stations_name = "parl.2019-12-12/Version 1/stations-merged.csv"
    addresses_name = "parl.2019-12-12/Version 1/addresses-merged.csv"
    elections = ["parl.2019-12-12"]
