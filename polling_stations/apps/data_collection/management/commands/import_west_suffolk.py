from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000245"
    addresses_name = "parl.2019-12-12/Version 2/Democracy club website data.csv"
    stations_name = "parl.2019-12-12/Version 2/Democracy club website data.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10094768454":
            return None

        if (uprn, record.addressline1) == ("10094064602", "26 Hambrook Close"):
            rec["postcode"] = "IP30 0UX"

        if record.addressline6 in [
            "IP31 2NY",
            "IP28 8WE",
            "IP33 1EE",
            "CB8 8BF",
        ]:
            return None
        return rec
