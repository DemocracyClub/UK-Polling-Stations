from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CLD"
    addresses_name = (
        "2023-05-04/2023-04-13T15:17:42.827927/Calderdale Polling Districts 2023.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-13T15:17:42.827927/Calderdale Polling Stations 2023.csv"
    )
    elections = ["2023-05-04"]
