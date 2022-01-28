from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = "2022-05-05/2022-01-28T16:01:05.704390/Democracy_Club__03February2022.tsv"
    stations_name = "2022-05-05/2022-01-28T16:01:05.704390/Democracy_Club__03February2022.tsv"
    elections = ['2022-05-05']
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
