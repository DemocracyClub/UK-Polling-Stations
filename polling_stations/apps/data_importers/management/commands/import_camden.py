from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CMD"
    addresses_name = (
        "2022-05-05/2022-04-05T16:06:41.598889/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-05T16:06:41.598889/Democracy Club - Polling Stations.csv"
    )
    elections = ["2022-05-05"]
