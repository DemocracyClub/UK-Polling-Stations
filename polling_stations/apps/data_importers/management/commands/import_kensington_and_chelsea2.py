from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000020"
    addresses_name = "2020-03-03T13:22:45.003848/Democracy_Club__07May2020.tsv"
    stations_name = "2020-03-03T13:22:45.003848/Democracy_Club__07May2020.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"
