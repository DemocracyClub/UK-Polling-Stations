from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E06000055"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy Club - Polling Districts UKPGE.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy Club - Polling Stations UKPGE.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    # KEMPSTON WEST METHODIST CHURCH Carried forward from local.2019-05-02
    def station_record_to_dict(self, record):
        if record.stationcode == "BAS_1":
            record = record._replace(xordinate="502614")
            record = record._replace(yordinate="247440")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        # Lot's of junk UPRNs
        record = record._replace(uprn="")

        rec = super().address_record_to_dict(record)

        if (
            uprn == "10024229957"
        ):  # MK442EY -> MK442EL : SKYLARKS, KIMBOLTON ROAD, BOLNHURST, BEDFORD
            rec["postcode"] = "MK442EL"

        if record.postcode in ["MK45 3PG", "MK45 3PW", "MK43 0BD"]:
            return None

        if record.add1 in [
            "CRIEGNESH",
            "THE SHIELING",
        ]:
            return None

        return rec
