from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000223"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019 (1).tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019 (1).tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "60031312":
            rec["postcode"] = "BN15 0RW"

        if record.addressline6 in ["BN41 1PL", "BN15 8LW"]:
            return None

        return rec
