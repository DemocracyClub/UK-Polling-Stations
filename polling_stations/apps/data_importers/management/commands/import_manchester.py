from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2024-09-05/2024-08-05T09:58:42.054002/Democracy_Club__05September2024.tsv"
    )
    stations_name = (
        "2024-09-05/2024-08-05T09:58:42.054002/Democracy_Club__05September2024.tsv"
    )
    elections = ["2024-09-05"]
    csv_delimiter = "\t"
