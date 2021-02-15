from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAW"
    addresses_name = "2021-01-25T10:50:55.656955/Tamworth_Borough_Council_Democracy_Club__06May2021.tsv"
    stations_name = "2021-01-25T10:50:55.656955/Tamworth_Borough_Council_Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
