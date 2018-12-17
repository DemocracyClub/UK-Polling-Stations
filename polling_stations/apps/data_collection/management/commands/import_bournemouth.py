from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E06000028"
    addresses_name = "local.bournemouth.throop-and-muscliff.by.2018-01-18/Version 1/local.bournemouth.throop-and-muscliff.by.2018-01-18.csv"
    stations_name = "local.bournemouth.throop-and-muscliff.by.2018-01-18/Version 1/local.bournemouth.throop-and-muscliff.by.2018-01-18.csv"
    elections = ["local.bournemouth.throop-and-muscliff.by.2018-01-18"]
    csv_encoding = "windows-1252"
