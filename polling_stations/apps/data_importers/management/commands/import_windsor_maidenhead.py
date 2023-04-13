from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WNM"
    addresses_name = (
        "2023-05-04/2023-04-13T15:19:53.305902/democracy club polling districts.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-13T15:19:53.305902/democracy club polling stations.csv"
    )
    elections = ["2023-05-04"]
