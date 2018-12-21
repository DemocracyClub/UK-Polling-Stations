from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000131"
    addresses_name = "Democracy_Club__04May2017 Harborough DC.TSV"
    stations_name = "Democracy_Club__04May2017 Harborough DC.TSV"
    elections = [
        "local.leicestershire.2017-05-04",
        #'parl.2017-06-08'
    ]
    csv_delimiter = "\t"
