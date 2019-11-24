from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000148"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-08Norwich.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-08Norwich.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode.strip() in ["NR4 7FW", "RG8 0RR", "NR6 5RP", "NR1 2EB"]:
            return None

        if uprn in ["10093501268", "100091562008"]:
            return None

        if uprn in [
            "100091553263"  # NR23AT -> NR23AU : ST JOHNS HOUSE 38 HEIGHAM ROAD, NORWICH
        ]:
            rec["accept_suggestion"] = True

        return rec
