from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOT"
    addresses_name = "2024-07-04/2024-06-07T16:41:56.977816/WOT_combined.tsv"
    stations_name = "2024-07-04/2024-06-07T16:41:56.977816/WOT_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"
