from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWM"
    addresses_name = (
        "2023-07-13/2023-06-16T10:52:14.592700/Democracy_Club__13July2023 (2).tsv"
    )
    stations_name = (
        "2023-07-13/2023-06-16T10:52:14.592700/Democracy_Club__13July2023 (2).tsv"
    )
    elections = ["2023-07-13"]
    csv_delimiter = "\t"
