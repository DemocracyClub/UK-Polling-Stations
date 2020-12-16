from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "W06000022"
    addresses_name = (
        "parl.2017-06-08/Version 1/Newport Democracy_Club__08June2017.tsv08June2017.tsv"
    )
    stations_name = (
        "parl.2017-06-08/Version 1/Newport Democracy_Club__08June2017.tsv08June2017.tsv"
    )
    # elections = ['parl.2017-06-08']
    csv_delimiter = "\t"
    csv_encoding = "latin-1"
