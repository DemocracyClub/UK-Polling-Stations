from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000087"
    addresses_name = "2020-02-03T10:02:24.726188/Democracy_Club__07May2020Fareham.tsv"
    stations_name = "2020-02-03T10:02:24.726188/Democracy_Club__07May2020Fareham.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"
