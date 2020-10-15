from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000092"
    addresses_name = "2020-02-10T11:07:21.390332/Democracy_Club__07May2020.tsv"
    stations_name = "2020-02-10T11:07:21.390332/Democracy_Club__07May2020.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"
