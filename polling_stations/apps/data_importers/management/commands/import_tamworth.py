from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAW"
    addresses_name = (
        "2024-07-04/2024-06-10T15:51:50.159605/Tamworth_Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-10T15:51:50.159605/Tamworth_Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"
