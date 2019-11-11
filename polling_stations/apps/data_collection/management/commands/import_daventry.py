from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000151"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019dave.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019dave.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "28052662":
            rec["postcode"] = "NN113QJ"

        if uprn in ["28061555", "28061556"]:
            return None

        return rec
