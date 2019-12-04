from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E06000022"
    addresses_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-22.csv"
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-22.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        # Addressbase has this postcode geolocated in the LA, however ONSPD doesn't.
        # This line is in to squash the
        # "Postcode centroid is outside target local authority" Warnings
        if record.housepostcode == "BA3 5SF":
            return None

        if uprn == "10093714167":
            rec["postcode"] = "BS140FF"

        if uprn == "10093715348":
            rec["postcode"] = "BS140FR"
            print("updating record")

        if uprn in ["10091550422"]:
            return None

        if record.houseid.strip() == "9006798":
            rec["postcode"] = "BS31 2FU"

        if record.houseid.strip() == "9014157":
            rec["postcode"] = "BS14 0FJ"

        if record.houseid.strip() == "9014290":
            rec["postcode"] = "BS14 0FH"

        if record.houseid.strip() == "9002893":
            rec["postcode"] = "BA2 0LH"

        if record.pollingstationnumber == "n/a":
            return None

        if record.uprn.strip() == "10001146303":
            rec["accept_suggestion"] = False

        if record.houseid.strip() == "9014616":
            rec["accept_suggestion"] = True

        return rec
