from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NUN"
    addresses_name = "2021-11-17T11:26:12.478111/Democracy_Club__25November2021.tsv"
    stations_name = "2021-11-17T11:26:12.478111/Democracy_Club__25November2021.tsv"
    elections = ["2021-11-25"]
    csv_delimiter = "\t"
