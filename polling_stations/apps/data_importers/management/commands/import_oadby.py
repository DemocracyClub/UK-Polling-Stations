from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OAD"
    addresses_name = "2023-05-04/2023-04-09T10:32:46.735243/Democracy_Club__04May2023 (Rev. 09-04-2023).tsv"
    stations_name = "2023-05-04/2023-04-09T10:32:46.735243/Democracy_Club__04May2023 (Rev. 09-04-2023).tsv"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"
