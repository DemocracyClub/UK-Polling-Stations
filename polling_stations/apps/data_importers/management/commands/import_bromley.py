from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRY"
    addresses_name = (
        "2021-04-13T11:41:45.130802/Bromley Democracy_Club__06May2021 (1).CSV"
    )
    stations_name = (
        "2021-04-13T11:41:45.130802/Bromley Democracy_Club__06May2021 (1).CSV"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"
