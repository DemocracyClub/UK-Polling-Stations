from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNT"
    addresses_name = "2024-05-02/2024-01-29T15:56:51.429272/nnt_test.tsv"
    stations_name = "2024-05-02/2024-01-29T15:56:51.429272/nnt_test.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
