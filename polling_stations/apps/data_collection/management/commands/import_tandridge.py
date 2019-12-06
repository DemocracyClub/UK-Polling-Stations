from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000215"
    addresses_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-26.csv"
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-26.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.houseid == "37666":
            rec["accept_suggestion"] = True
        if record.houseid == "37412":
            rec["accept_suggestion"] = False
        if record.housepostcode in ["CR8 5AT", "RH7 6BL"]:
            return None

        return rec

    def station_record_to_dict(self, record):

        # Outside the LA area
        if record.pollingstationnumber in [
            "38",
            "40",
            "35",
            "34",
            "41",
            "37",
        ]:
            return None

        return super().station_record_to_dict(record)
