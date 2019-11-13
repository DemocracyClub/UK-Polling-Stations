from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000224"
    addresses_name = (
        "parl.2019-12-12/Version 1/elections@arun.gov.uk-1572944623000-.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/elections@arun.gov.uk-1572944623000-.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False
