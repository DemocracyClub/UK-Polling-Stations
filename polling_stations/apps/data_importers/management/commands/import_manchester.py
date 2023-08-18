from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2023-09-07/2023-08-18T16:50:24.008176/Democracy_Club__07September2023.tsv"
    )
    stations_name = (
        "2023-09-07/2023-08-18T16:50:24.008176/Democracy_Club__07September2023.tsv"
    )
    elections = ["2023-09-07"]
    csv_delimiter = "\t"
