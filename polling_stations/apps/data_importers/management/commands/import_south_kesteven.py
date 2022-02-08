from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = "2022-02-24/2022-02-08T14:16:28.018438/Democracy_Club__24February2022.tsv"
    stations_name = "2022-02-24/2022-02-08T14:16:28.018438/Democracy_Club__24February2022.tsv"
    elections = ['2022-02-24']
    csv_delimiter = "\t"
