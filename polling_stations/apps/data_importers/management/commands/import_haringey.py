from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRY"
    addresses_name = (
        "2023-10-04/2023-09-13T17:37:20.361423/Democracy_Club__04October2023.tsv"
    )
    stations_name = (
        "2023-10-04/2023-09-13T17:37:20.361423/Democracy_Club__04October2023.tsv"
    )
    elections = ["2023-10-04"]
    csv_delimiter = "\t"
