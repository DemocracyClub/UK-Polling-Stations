from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAW"
    addresses_name = (
        "2023-10-19/2023-10-06T15:01:41.548647/Democracy_Club__19October2023.tsv"
    )
    stations_name = (
        "2023-10-19/2023-10-06T15:01:41.548647/Democracy_Club__19October2023.tsv"
    )
    elections = ["2023-10-19"]
    csv_delimiter = "\t"
