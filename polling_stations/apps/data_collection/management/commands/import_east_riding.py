from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E06000011"
    addresses_name = "parl.2019-12-12/Version 1/Democracy Club - Polling Districts.csv"
    stations_name = "parl.2019-12-12/Version 1/Democracy Club - Polling Stations.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.add1 == "GOWTHORPE FIELDS HATKILL LANE":
            rec["postcode"] = "YO411HR"

        if record.add1 in [
            "M. V. Sabina H.",
            "Alcuin College",
        ]:
            return None

        if uprn in [
            "100052164542",
            "100050024437",
        ]:
            return None

        return rec
