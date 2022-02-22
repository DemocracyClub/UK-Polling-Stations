from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAT"
    addresses_name = "2022-05-05/2022-02-22T09:04:34.675651/Democracy_Club__05May2022.tsv"
    stations_name = "2022-05-05/2022-02-22T09:04:34.675651/Democracy_Club__05May2022.tsv"
    elections = ['2022-05-05']
    csv_delimiter = "\t"
