"""
Imports Camden
"""


from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CMD"
    addresses_name = "2021-03-24T10:52:03.478834/Democracy Club Polling Districts.csv"
    stations_name = "2021-03-24T10:52:03.478834/Democracy Club polling stations.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.stationcode == "MB_1":
            record = record._replace(postcode="NW1 7EA")

        return super().station_record_to_dict(record)
