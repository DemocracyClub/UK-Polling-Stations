from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PRE"
    addresses_name = "2024-07-04/2024-07-02T21:06:16.716380/RIBBLE VALLEY Democracy_Club__04July2024.tsv"
    stations_name = "2024-07-04/2024-07-02T21:06:16.716380/RIBBLE VALLEY Democracy_Club__04July2024.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"
