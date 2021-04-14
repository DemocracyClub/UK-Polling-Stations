from data_importers.ems_importers import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FIF"
    addresses_name = "2021-04-12T09:21:22.730934/Fife E8 DC Polling Districts.csv"
    stations_name = "2021-04-12T09:21:22.730934/Fife E8 DC Polling Stations.csv"
    elections = ["2021-05-06"]
