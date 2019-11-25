from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000058"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019BCP.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019BCP.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False
