from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "W06000004"
    addresses_name = (
        "parl.maybe/Version 1/denbighshire-Democracy_Club__15October2019.tsv"
    )
    stations_name = (
        "parl.maybe/Version 1/denbighshire-Democracy_Club__15October2019.tsv"
    )
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    elections = ["parl.maybe"]

    def get_station_point(self, record):
        return None
