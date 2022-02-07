from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ABD"
    addresses_name = "2022-05-05/2022-02-07T18:54:39.429722/wdiv-upload-test.tsv"
    stations_name = "2022-05-05/2022-02-07T18:54:39.429722/wdiv-upload-test.tsv"
    elections = ['2022-05-05']
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
