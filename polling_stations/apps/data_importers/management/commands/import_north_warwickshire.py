from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWA"
    addresses_name = "2022-05-05/2022-02-09T09:44:57.344590/Democracy_Club__06May2021.tsv"
    stations_name = "2022-05-05/2022-02-09T09:44:57.344590/Democracy_Club__06May2021.tsv"
    elections = ['2022-05-05']
    csv_delimiter = "\t"
