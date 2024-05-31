from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "VGL"
    addresses_name = (
        "2024-07-04/2024-06-06T10:32:09.163599/polling-districts-combined.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-06T10:32:09.163599/polling-stations-combined.csv"
    )
    elections = ["2024-07-04"]
