from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = "2026-10-01/2026-08-24T10:30:32.968228/Democracy Club - Polling Districts W3.csv"
    stations_name = (
        "2026-10-01/2026-08-24T10:30:32.968228/Democracy Club - Polling Stations W3.csv"
    )
    elections = ["2026-10-01"]
    csv_encoding = "utf-16le"

    # maintaining exclusions through by-election

    # def address_record_to_dict(self, record):
    #     uprn = record.uprn.strip().lstrip("0")

    #     if (
    #         uprn
    #         in [
    #             "130128845",  # MELLNESS HOUSE, GLEN URQUHART, DRUMNADROCHIT, INVERNESS, IV63 6TW
    #             "130000426",  # 22 NESS ROAD, FORTROSE, IV10 8SD
    #             "130147608",  # NEWLANDS OF URCHANY, NAIRN
    #         ]
    #     ):
    #         return None

    #     if record.postcode in [
    #         # looks wrong
    #         "PH33 6FP",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)
