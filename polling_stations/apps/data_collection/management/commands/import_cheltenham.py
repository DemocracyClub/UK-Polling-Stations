from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000078"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-08chelt.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-08chelt.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn in ["100121231365", "100121231366"]:
            rec["postcode"] = "GL51 6QL"
            return rec

        if uprn == "100120389274":
            rec["postcode"] = "GL52 2BT"
            return rec

        if record.houseid in ["63059", "54850"]:
            return None

        if uprn in [
            "200002683968",
            "200002683961",
            "10024305502",
        ]:
            return None

        return rec
