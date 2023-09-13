from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAW"
    addresses_name = (
        "2023-10-05/2023-09-13T17:02:57.869201/Democracy_Club__19October2023.tsv"
    )
    stations_name = (
        "2023-10-05/2023-09-13T17:02:57.869201/Democracy_Club__19October2023.tsv"
    )
    elections = ["2023-10-05"]
    csv_delimiter = "\t"
