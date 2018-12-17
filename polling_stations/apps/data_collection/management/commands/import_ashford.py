from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000105"
    addresses_name = (
        "parl.2017-06-08/Version 2/Ashford Democracy_Club__08June2017-2.tsv"
    )
    stations_name = "parl.2017-06-08/Version 2/Ashford Democracy_Club__08June2017-2.tsv"
    elections = ["parl.2017-06-08"]
    csv_delimiter = "\t"
