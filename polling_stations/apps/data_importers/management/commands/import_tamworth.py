from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAW"
    addresses_name = "2024-05-02/2024-02-06T16:47:08.334955/Tamworth_Borough_Council_Democracy_Club__02May2024.tsv"
    stations_name = "2024-05-02/2024-02-06T16:47:08.334955/Tamworth_Borough_Council_Democracy_Club__02May2024.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
