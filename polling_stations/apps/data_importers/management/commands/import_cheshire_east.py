from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHE"
    addresses_name = (
        "2024-02-08/2024-01-30T11:09:16.652912/Democracy_Club__08February2024.tsv"
    )
    stations_name = (
        "2024-02-08/2024-01-30T11:09:16.652912/Democracy_Club__08February2024.tsv"
    )
    elections = ["2024-02-08"]
    csv_delimiter = "\t"
