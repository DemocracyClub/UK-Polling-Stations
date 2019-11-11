from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000142"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019WL.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019WL.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False
