from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "TEN"
    addresses_name = "2024-05-02/2024-03-25T14:34:45.437403/DC Polling Districts.csv"
    stations_name = "2024-05-02/2024-03-25T14:34:45.437403/DC Polling stations.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"
