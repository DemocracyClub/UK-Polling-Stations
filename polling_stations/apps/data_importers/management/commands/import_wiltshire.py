from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIL"
    addresses_name = (
        "2024-03-14/2024-03-12T12:46:49.832143/Democracy_Club__14March2024.tsv"
    )
    stations_name = (
        "2024-03-14/2024-03-12T12:46:49.832143/Democracy_Club__14March2024.tsv"
    )
    elections = ["2024-03-14"]
    csv_delimiter = "\t"
