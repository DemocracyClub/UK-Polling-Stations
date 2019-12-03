from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000236"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019-Redditch.CSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019-Redditch.CSV"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        if record.addressline6 == "B96 6RN":
            return None  # centroid outside authority

        if (record.addressline1, record.addressline2) == (
            "4A High Street",
            "Feckenham",
        ):
            record = record._replace(property_urn="100121268977")

        if record.addressline6 == "B98 9BH":
            record = record._replace(addressline6="B98 9BJ")
        if record.addressline6 == "B67 6QA":
            record = record._replace(addressline6="B97 6QA")

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100120640565":
            rec["postcode"] = "B98 9PJ"
            rec["accept_suggestion"] = False

        return rec
