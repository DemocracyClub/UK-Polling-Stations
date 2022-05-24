from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WKF"
    addresses_name = "2022-06-23/2022-05-24T13:35:14.816630/Democracy Club - Polling Districts - June 2022 Parliamentary By Election Wakefield.csv"
    stations_name = "2022-06-23/2022-05-24T13:35:14.816630/Democracy Club - Polling Stations - June 2022 Parliamentary By Election Wakefield.csv"
    elections = ['2022-06-23']
