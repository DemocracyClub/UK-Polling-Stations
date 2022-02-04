from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = "2022-02-24/2022-02-04T19:02:15.791409/Democracy_Club__03February2022.tsv"
    stations_name = "2022-02-24/2022-02-04T19:02:15.791409/Democracy_Club__03February2022.tsv"
    elections = ['2022-02-24']
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
