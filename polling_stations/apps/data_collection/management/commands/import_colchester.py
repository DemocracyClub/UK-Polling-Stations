from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000071"
    addresses_name = "parl.2019-12-12/Version 1/colchester.gov.uk-1573052308000-.csv"
    stations_name = "parl.2019-12-12/Version 1/colchester.gov.uk-1573052308000-.csv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = ","
    allow_station_point_from_postcode = False
