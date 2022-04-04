from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYE"
    addresses_name = "2022-05-05/2022-04-04T13:14:14.289778/Democracy_Club__05May2022-3.tsv"
    stations_name = "2022-05-05/2022-04-04T13:14:14.289778/Democracy_Club__05May2022-3.tsv"
    elections = ['2022-05-05']
    csv_delimiter = "\t"
