from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIN"
    addresses_name = "2023-05-04/2023-03-30T13:36:19.020481/ems_exports_combined.tsv"
    stations_name = "2023-05-04/2023-03-30T13:36:19.020481/ems_exports_combined.tsv"
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
