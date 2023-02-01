from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLA"
    addresses_name = (
        "2023-02-09/2023-02-01T10:29:45.813431/Democracy_Club__09February2023.CSV"
    )
    stations_name = (
        "2023-02-09/2023-02-01T10:29:45.813431/Democracy_Club__09February2023.CSV"
    )
    elections = ["2023-02-09"]
