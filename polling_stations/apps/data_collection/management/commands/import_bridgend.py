from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "W06000013"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-08bridgend.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-08bridgend.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn == "10090816154":
            rec["postcode"] = "CF365HN"
        if uprn == "10090815370":
            rec["postcode"] = "CF320EP"
        if uprn == "10090814759":
            rec["postcode"] = "CF356FR"

        if record.housepostcode in ["CF33 4RY", "CF32 0NR"]:
            return None

        return rec
