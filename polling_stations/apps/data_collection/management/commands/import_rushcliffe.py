from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000176"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # these co-ordinates were a missing a digit - fixes carried over from local.2019-05-02
        if record.polling_place_id == "4566":  # Bingham Methodist Centre
            record = record._replace(polling_place_easting="470360")
        if record.polling_place_id == "4660":  # Edwalton Church Hall
            record = record._replace(polling_place_easting="459770")
        if record.polling_place_id == "4785":  # West Bridgford Baptist Church
            record = record._replace(polling_place_easting="458380")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "3040072549":
            rec["postcode"] = "NG2 7PQ"
            rec["accept_suggestion"] = False

        return rec
