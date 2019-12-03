from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E09000013"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-16H&F.csv"
    )
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-16H&F.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "34157887":
            rec["postcode"] = "W60BY"

        if uprn in [
            "34148072",
            "34136009",
            "34135797",
            "34129561",
            "34155328",
        ]:
            return None

        if (record.housenumber, record.streetname) == ("17A", "Hannell Road"):
            return None

        if record.housepostcode in [
            "NW10 6FG",
            "W12 8HH",
        ]:
            return None

        return rec
