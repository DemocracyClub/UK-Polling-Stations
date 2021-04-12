from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUH"
    addresses_name = "2021-03-25T09:29:47.041150/Rushmoor Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-25T09:29:47.041150/Rushmoor Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
