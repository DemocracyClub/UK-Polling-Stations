from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BDF"
    addresses_name = "2023-05-04/2023-02-27T10:40:20.843815/Bedford Polling Districts - Democracy Club.csv"
    stations_name = "2023-05-04/2023-02-27T10:40:20.843815/Bedford Polling Stations for Democracy Club.csv"
    elections = ["2023-05-04"]
