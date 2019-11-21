from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "W06000003"
    addresses_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019_20.11.2019.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019_20.11.2019.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False
