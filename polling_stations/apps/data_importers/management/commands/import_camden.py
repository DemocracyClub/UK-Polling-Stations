from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CMD"
    addresses_name = (
        "2024-05-02/2024-03-25T13:12:33.651843/DC Clubs_PollingDistricts_CAMDEN.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-25T13:12:33.651843/DC Clubs_PollingStations_CAMDEN.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"
