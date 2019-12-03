from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000156"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019welling.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019welling.csv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False
