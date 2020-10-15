from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000119"
    addresses_name = "2020-02-10T11:11:39.774936/Democracy_Club__07May2020 Fylde.CSV"
    stations_name = "2020-02-10T11:11:39.774936/Democracy_Club__07May2020 Fylde.CSV"
    elections = ["2020-05-07"]
