from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EDE"
    addresses_name = "2022-06-23/2022-05-31T10:17:07.773032/Democracy_Club__23June2022 new.tsv"
    stations_name = "2022-06-23/2022-05-31T10:17:07.773032/Democracy_Club__23June2022 new.tsv"
    elections = ['2022-06-23']
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
