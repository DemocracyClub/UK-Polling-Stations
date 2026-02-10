from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "VGL"
    addresses_name = "2026-05-07/2026-02-10T14:52:58.106281/Democracy Club Polling Districts VoG 2.csv"
    stations_name = "2026-05-07/2026-02-10T14:52:58.106281/Democracy Club Polling Stations VoG 2.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # Removing bad coordinates for:
        # ST CATTWGS VILLAGE HALL, SIGINSTONE LANE, LLANMAES, VALE OF GLAMORGAN CF61 2XR
        if record.stationcode == "72":
            record = record._replace(
                xordinate="",
                yordinate="",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "CF62 6BA",
        ]:
            return None

        return super().address_record_to_dict(record)
