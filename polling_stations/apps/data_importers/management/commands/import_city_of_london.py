from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "LND"
    addresses_name = (
        "2024-07-04/2024-05-31T09:20:13.426583/CoL DemClub Polling Districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-05-31T09:20:13.426583/CoL DemClub Polling Stations.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"
