from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000009"
    addresses_name = "parl.2019-12-12/Version 1/districts-merged.csv"
    stations_name = "parl.2019-12-12/Version 1/stations-merged.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        if record.stationcode == "LE1":
            # KENNETT PAVILION
            record = record._replace(postcode="CB8 7QF")

        # Station codes that don't have any addresses pointing to them and are
        # mostly outside the LA, but are probably used by other LAs. Anyway it
        # reduces the warning flood.
        if record.stationcode in (
            "OA1/1",
            "OA1/2",
            "OA2",
            "OA3",
            "OA4",
            "OB1",
            "OC1",
            "OC1 (OC2)",
            "OC2",
            "OD1/1",
            "OD1/2",
            "OD2",
            "RA1 RA2",
            "RB1/1",
            "RB1/2",
            "RC1",
            "RD1",
            "RE1",
            "RE2",
            "RG1",
            "SB1",
            "SD1",
            "SD1 (SD2)",
            "SD2",
            "ZA1",
            "ZB1",
            "ZD1",
            "ZE1",
            "ZF1",
            "ZG1/1",
            "ZG1/2",
            "ZH1",
            "ZI1",
            "ZJ1",
            "ZK1",
            "RG2",
        ):
            return None

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if "dummy" in record.add1.lower():
            return None

        if uprn in [
            "10002605543",  # 51 HILL PARK CRESCENT, PLYMOUTH, CITY OF PLYMOUTH
            "10002600979",  # 774 NEWMARKET ROAD, TEVERSHAM, CAMBRIDGESHIRE
        ]:
            return None

        if uprn in [
            "10002591793",  # CB62DS -> CB62BU : HALE FEN HOUSE, 1 HALE FEN LANE, WARDY HILL, ELY
            "100091191582",  # CB80TS -> CB80UU : 2 GATEHOUSE COTTAGES, LOWER HARE PARK, LONDON ROAD, STETCHWORTH, NEWMARKET
        ]:
            rec["accept_suggestion"] = False

        return rec
