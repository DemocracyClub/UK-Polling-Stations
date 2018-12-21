from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "W06000006"
    addresses_name = "parl.2017-06-08/Version 1/Wrexham Democracy_Club__08June2017.CSV"
    stations_name = "parl.2017-06-08/Version 1/Wrexham Democracy_Club__08June2017.CSV"
    elections = ["parl.2017-06-08"]
