from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000017"
    addresses_name = "2020-02-19T10:04:28.162348/Democracy_Club__07May2020...TSV"
    stations_name = "2020-02-19T10:04:28.162348/Democracy_Club__07May2020...TSV"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"
