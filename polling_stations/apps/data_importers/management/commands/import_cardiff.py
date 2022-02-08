from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRF"
    addresses_name = "2022-02-17/2022-02-08T14:29:57.137736/wdiv-upload-test.tsv"
    stations_name = "2022-02-17/2022-02-08T14:29:57.137736/wdiv-upload-test.tsv"
    elections = ['2022-02-17']
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
