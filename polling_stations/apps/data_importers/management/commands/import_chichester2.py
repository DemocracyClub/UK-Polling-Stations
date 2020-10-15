from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000225"
    addresses_name = "2020-02-12T10:50:30.802114/Democracy_Club__07May2020chi.tsv"
    stations_name = "2020-02-12T10:50:30.802114/Democracy_Club__07May2020chi.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"
