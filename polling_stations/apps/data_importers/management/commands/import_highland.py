from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = "2026-05-07/2026-02-16T17:20:11.291474/Democracy Club - Polling Districts Highland SPE.csv"
    stations_name = "2026-05-07/2026-02-16T17:20:11.291474/Democracy Club - Polling Stations Highland SPE.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # station change from council:
        # OLD: SHIELBRIDGE HALL ACHARACLE PH36 4JL
        # NEW: Acharcle Primary - Acharacle, Argyll, PH36 4JU
        if record.stationcode == "SLB103":
            record = record._replace(
                xordinate="167465",
                yordinate="768113",
                placename="Acharcle Primary",
                add1="",
                add2="Acharacle",
                add3="Argyll",
                postcode="PH36 4JU",
            )

        # coord fix from council for:
        # The Green Hall, Sinclair Terrace, Smithton, Inverness, IV2 7NP
        if record.stationcode in [
            "IN42",
            "IN43",
        ]:
            record = record._replace(
                xordinate="271300",
                yordinate="845865",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "130128845",  # MELLNESS HOUSE, GLEN URQUHART, DRUMNADROCHIT, INVERNESS, IV63 6TW
                "130000426",  # 22 NESS ROAD, FORTROSE, IV10 8SD
                "130147608",  # NEWLANDS OF URCHANY, NAIRN
            ]
        ):
            return None

        if record.postcode in [
            # looks wrong
            "PH33 6FP",
        ]:
            return None

        return super().address_record_to_dict(record)
