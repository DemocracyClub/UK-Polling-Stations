from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SFT"
    addresses_name = (
        "2024-07-04/2024-06-28T11:36:11.728532/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-28T11:36:11.728532/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"
