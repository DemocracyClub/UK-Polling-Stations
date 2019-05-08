from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E09000005"
    addresses_name = "europarl.2019-05-23/Version 1/DC PD.csv"
    stations_name = "europarl.2019-05-23/Version 1/DC PS.csv"
    elections = ["europarl.2019-05-23"]
