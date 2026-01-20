from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLV"
    addresses_name = "2026-05-07/2026-01-20T16:51:22.129100/Democracy_Club Wolverhampton Polling Stations__07May2026.tsv"
    stations_name = "2026-05-07/2026-01-20T16:51:22.129100/Democracy_Club Wolverhampton Polling Stations__07May2026.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
