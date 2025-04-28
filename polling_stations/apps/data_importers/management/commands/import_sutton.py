from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STN"
    addresses_name = (
        "2025-05-22/2025-04-28T09:58:32.350706/Democracy Club- Polling Districts.csv"
    )
    stations_name = (
        "2025-05-22/2025-04-28T09:58:32.350706/Democracy clubs- Polling stations.csv"
    )
    elections = ["2025-05-22"]
    csv_encoding = "utf-16le"

    # By-election, Maintaining unused script changes as comment for future reference:
    # def station_record_to_dict(self, record):
    #     # more accurate point for: Holy Trinity Church Centre, Maldon Road, Wallington, SM6 8BL
    #     if record.stationcode in ["RB/1", "RB/2"]:
    #         rec = super().station_record_to_dict(record)
    #         rec["location"] = Point(-0.151435, 51.364474, srid=4326)
    #         return rec

    #     return super().station_record_to_dict(record)
