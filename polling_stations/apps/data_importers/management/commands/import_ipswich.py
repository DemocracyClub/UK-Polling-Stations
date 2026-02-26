from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IPS"
    addresses_name = (
        "2026-05-07/2026-02-26T10:30:43.578981/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-02-26T10:30:43.578981/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
