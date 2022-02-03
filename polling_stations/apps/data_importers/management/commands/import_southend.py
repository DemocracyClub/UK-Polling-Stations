from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = "2022-05-05/2022-02-03T11:09:22.973906/Democracy_Club__03February2022.tsv"
    stations_name = "2022-05-05/2022-02-03T11:09:22.973906/Democracy_Club__03February2022.tsv"
    elections = ['2022-05-05']
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
