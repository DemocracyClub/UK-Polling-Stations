from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000082"
    addresses_name = (
        "parl.2017-06-08/Version 1/Stroud Democracy Club - Where Do I Vote.TSV"
    )
    stations_name = (
        "parl.2017-06-08/Version 1/Stroud Democracy Club - Where Do I Vote.TSV"
    )
    elections = ["parl.2017-06-08"]
    csv_encoding = "latin-1"
    csv_delimiter = "\t"
