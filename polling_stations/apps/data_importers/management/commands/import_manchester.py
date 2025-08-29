from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2025-09-25/2025-08-29T13:17:31.958974/Democracy_Club__25September2025.tsv"
    )
    stations_name = (
        "2025-09-25/2025-08-29T13:17:31.958974/Democracy_Club__25September2025.tsv"
    )
    elections = ["2025-09-25"]
    csv_delimiter = "\t"
