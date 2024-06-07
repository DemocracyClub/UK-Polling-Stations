from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GOS"
    addresses_name = (
        "2024-07-04/2024-06-07T13:16:42.794107/Gosport-Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-07T13:16:42.794107/Gosport-Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"
