from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "KTT"
    addresses_name = "2022-05-05/2022-04-08T10:23:22.521537/RBK_Polling Districs.csv"
    stations_name = "2022-05-05/2022-04-08T10:23:22.521537/RBK_Polling Stations.csv"
    elections = ["2022-06-23"]
