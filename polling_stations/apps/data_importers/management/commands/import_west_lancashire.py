from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLA"
    addresses_name = (
        "2023-06-22/2023-06-19T12:35:32.496297/Democracy_Club__22June2023.tsv"
    )
    stations_name = (
        "2023-06-22/2023-06-19T12:35:32.496297/Democracy_Club__22June2023.tsv"
    )
    elections = ["2023-06-22"]
    csv_delimiter = "\t"
