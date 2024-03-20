from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAW"
    addresses_name = "2024-05-02/2024-03-20T13:40:40.110534/Tamworth_Borough_Council_Democracy_Club__02May2024 v2.tsv"
    stations_name = "2024-05-02/2024-03-20T13:40:40.110534/Tamworth_Borough_Council_Democracy_Club__02May2024 v2.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
