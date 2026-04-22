from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "VGL"
    addresses_name = "2026-05-07/2026-04-22T15:31:44.783961/VGL_Districts_combined.csv"
    stations_name = "2026-05-07/2026-04-22T15:31:44.783961/VGL_Stations_combined.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # Fixing bad coordinates for:
        # ST CATTWGS VILLAGE HALL, SIGINSTONE LANE, LLANMAES, VALE OF GLAMORGAN CF61 2XR
        if record.stationcode == "72":
            record = record._replace(
                xordinate="298052",
                yordinate="169848",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "64118392",  # LONGBOAT, KNOLL CLOSE, COG ROAD, SULLY, PENARTH
            "200001640409",  # TY BWCH, DINGLE LANE, PENARTH
        ]:
            return None
        if record.postcode in [
            # split
            "CF62 6BA",
        ]:
            return None

        return super().address_record_to_dict(record)
