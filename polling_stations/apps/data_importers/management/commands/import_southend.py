from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = "2022-03-03/2022-01-28T16:40:33.252073/Democracy_Club__03February2022.tsv"
    stations_name = "2022-03-03/2022-01-28T16:40:33.252073/Democracy_Club__03February2022.tsv"
    elections = ['2022-03-03']
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
