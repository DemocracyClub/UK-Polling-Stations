from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000094"
    addresses_name = "WinchesterDemocracy_Club__04May2017 (2).tsv"
    stations_name = "WinchesterDemocracy_Club__04May2017 (2).tsv"
    elections = [
        "local.hampshire.2017-05-04",
        #'parl.2017-06-08'
    ]
    csv_delimiter = "\t"
