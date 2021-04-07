from data_importers.ems_importers import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ELS"
    addresses_name = "2021-04-06T12:11:19.403100/Democracy Club - Polling Districts Western Isles.csv"
    stations_name = (
        "2021-04-06T12:11:19.403100/Democracy Club - Polling Stations Western Isles.csv"
    )
    elections = ["2021-05-06"]
