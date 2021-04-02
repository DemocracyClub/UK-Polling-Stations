from data_importers.ems_importers import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DGY"
    addresses_name = (
        "2021-04-01T10:19:31.362798/D&GPollingDistrics_DemocractClub250321.csv"
    )
    stations_name = (
        "2021-04-01T10:19:31.362798/D&GPollingStations_DemocractClub250321.csv"
    )
    elections = ["2021-05-06"]
