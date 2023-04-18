from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SHE"
    addresses_name = "2023-05-04/2023-04-18T10:57:30.072283/Polling District - Folkestone and Hythe (1).csv"
    stations_name = "2023-05-04/2023-04-18T10:57:30.072283/Polling Stations - Folkestone and Hythe.csv"
    elections = ["2023-05-04"]
