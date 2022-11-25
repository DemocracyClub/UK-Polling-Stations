from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = (
        "2022-12-15/2022-11-25T14:34:32.124360/Democracy_Club__15December2022.tsv"
    )
    stations_name = (
        "2022-12-15/2022-11-25T14:34:32.124360/Democracy_Club__15December2022.tsv"
    )
    elections = ["2022-12-15"]
    csv_delimiter = "\t"
