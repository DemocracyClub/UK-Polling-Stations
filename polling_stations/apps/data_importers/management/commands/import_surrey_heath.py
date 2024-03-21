from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SUR"
    addresses_name = "2024-05-02/2024-03-21T20:01:29.277910/Democracy_Club__02May2024 Surrey Heath.tsv"
    stations_name = "2024-05-02/2024-03-21T20:01:29.277910/Democracy_Club__02May2024 Surrey Heath.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
