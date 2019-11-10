from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "W06000011"
    addresses_name = "parl.2019-12-12/Version 2/polling_station_export-2019-11-06.csv"
    stations_name = "parl.2019-12-12/Version 2/polling_station_export-2019-11-06.csv"
    elections = ["parl.2019-12-12"]
    csv_encoding = "latin-1"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.pollingstationaddress_5 == "mail@clydach.wales":
            record = record._replace(pollingstationaddress_5="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode == "SA2 OSF":
            rec["postcode"] = "SA2 0SF"
        if record.housepostcode == "SA2 OLY":
            rec["postcode"] = "SA2 0LY"
        if record.housepostcode == "SA2 OPN":
            rec["postcode"] = "SA2 0PN"
        if record.housepostcode == "SAG 5PG":
            rec["postcode"] = "SA6 5PG"

        if uprn in ["10010062487", "10010062488"]:
            rec["accept_suggestion"] = False

        return rec
