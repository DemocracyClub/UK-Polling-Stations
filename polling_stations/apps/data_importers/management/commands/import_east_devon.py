from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EDE"
    addresses_name = "2022-06-23/2022-05-30T15:41:34.577745/Democracy_Club__23June2022 (1).tsv"
    stations_name = "2022-06-23/2022-05-30T15:41:34.577745/Democracy_Club__23June2022 (1).tsv"
    elections = ['2022-06-23']
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
