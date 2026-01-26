from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLV"
    addresses_name = "2026-05-07/2026-01-22T16:58:37.246479/Update - Democracy_Club Wolverhampton 07May2026.tsv"
    stations_name = "2026-05-07/2026-01-22T16:58:37.246479/Update - Democracy_Club Wolverhampton 07May2026.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
