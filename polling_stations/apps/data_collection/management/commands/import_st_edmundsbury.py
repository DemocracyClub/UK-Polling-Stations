from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000204"
    addresses_name = "St_Edmundsbury_split.csv"
    stations_name = "St_Edmundsbury_split.csv"
    elections = ["local.suffolk.2017-05-04", "parl.2017-06-08"]
