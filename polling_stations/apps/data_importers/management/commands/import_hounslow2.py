from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000018"
    addresses_name = "2020-02-19T09:58:45.236148/Democracy_Club__7 May 2020.CSV"
    stations_name = "2020-02-19T09:58:45.236148/Democracy_Club__7 May 2020.CSV"
    elections = ["2020-05-07"]
    csv_encoding = "windows-1252"
