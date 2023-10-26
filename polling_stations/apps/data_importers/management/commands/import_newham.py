from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWM"
    addresses_name = (
        "2023-11-23/2023-10-26T16:14:56.962812/Democracy_Club__23November2023.tsv"
    )
    stations_name = (
        "2023-11-23/2023-10-26T16:14:56.962812/Democracy_Club__23November2023.tsv"
    )
    elections = ["2023-11-23"]
    csv_delimiter = "\t"
