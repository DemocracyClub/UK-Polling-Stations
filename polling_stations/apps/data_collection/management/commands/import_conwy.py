from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "W06000003"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019_Conwy.CSV"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019_Conwy.CSV"
    elections = ["europarl.2019-05-23"]
