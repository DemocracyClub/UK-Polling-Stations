from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "KTT"
    addresses_name = "2022-11-10/2022-10-24T10:18:05.344501/RBK_Polling Districts_GreenLane&StJames.csv"
    stations_name = "2022-11-10/2022-10-24T10:18:05.344501/RBK_Polling Stations_GreenLane&StJames.csv"
    elections = ["2022-11-10"]
