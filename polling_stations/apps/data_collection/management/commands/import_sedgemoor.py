from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000188"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-11sedge.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-11sedge.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()
        rec = super().address_record_to_dict(record)

        if uprn == "200000451332":
            rec["postcode"] = "TA7 0SD"

        if uprn == "200000450011":
            rec["postcode"] = "BS26 2HU"

        if record.housepostcode in [
            "TA5 1NQ",
            "TA5 1NG",
            "TA5 1JW",
        ]:
            return None

        return rec
