from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MDE"
    addresses_name = "2022-06-23/2022-05-27T11:08:28.486876/Democracy_Club__23June2022.tsv"
    stations_name = "2022-06-23/2022-05-27T11:08:28.486876/Democracy_Club__23June2022.tsv"
    elections = ['2022-06-23']
    csv_delimiter = "\t"
