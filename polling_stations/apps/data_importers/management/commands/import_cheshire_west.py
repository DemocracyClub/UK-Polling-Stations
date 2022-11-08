from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHW"
    addresses_name = "2022-12-01/2022-11-08T15:48:41.270054/City of Chester by-election Democracy_Club__01December2022.CSV"
    stations_name = "2022-12-01/2022-11-08T15:48:41.270054/City of Chester by-election Democracy_Club__01December2022.CSV"
    elections = ["2022-12-01"]
