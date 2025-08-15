from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = "2025-09-25/2025-08-15T17:03:14.048388/Democracy Club - Polling Districts W7 & W11.csv"
    stations_name = "2025-09-25/2025-08-15T17:03:14.048388/Democracy Club - Polling Stations W7 & W11.csv"
    elections = ["2025-09-25"]
    csv_encoding = "utf-16le"

    # Maintaining exclusions through by-election

    def station_record_to_dict(self, record):
        # # correcting obviously wrong point for:
        # # CROWN CHURCH, INVERNESS, KINGSMILLS ROAD, INVERNESS
        # if record.stationcode in [
        #     "I085",
        #     "I086",
        # ]:
        #     record = record._replace(xordinate="267087")

        # # SCOURIE COMMUNITY HALL, SCOURIE, LAIRG, SUTHERLAND, IV27 4TE
        # if record.stationcode == "C006":
        #     record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        # uprn = record.uprn.strip().lstrip("0")

        # if (
        #     uprn
        #     in [
        #         "130150387",  # MILL COTTAGE A863 B884 JUNCTION - A850 JUNCTION, KILMUIR, DUNVEGAN
        #         "130186635",  # 1 MACFARLANE BUILDINGS, CRUACHAN PLACE, PORTREE
        #         "130131942",  # 3 WOODLAND PARK, CONTIN
        #         "130178830",  # 12 COUNTY PLACE, CULDUTHEL, INVERNESS
        #         "130197101",  # 4 BLACK ISLE VIEW, STRATTON, INVERNESS
        #         "130147608",  # NEWLANDS OF URCHANY, NAIRN
        #     ]
        # ):
        #     return None

        # if record.postcode in [
        #     # split
        #     "IV17 0QY",
        #     "IV23 2RW",
        # ]:
        #     return None
        return super().address_record_to_dict(record)
