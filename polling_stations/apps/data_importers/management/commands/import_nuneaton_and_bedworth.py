from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NUN"
    addresses_name = "2024-05-02/2024-01-29T16:58:19.509270/NUN_test.tsv"
    stations_name = "2024-05-02/2024-01-29T16:58:19.509270/NUN_test.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
