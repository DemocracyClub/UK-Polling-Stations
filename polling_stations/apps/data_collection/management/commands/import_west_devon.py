from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000047"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10001329690"  # EX201SQ -> EX201JJ : Beechwood, Upcott Hill, Okehampton, Devon
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        # Charter Hall (Polling Station No.1-4)
        if record.polling_place_id in ["6965", "6975", "6971", "6973"]:
            record = record._replace(polling_place_uprn="10013752301")

        # Milton Abbot Village Halls
        if record.polling_place_id == "7237":
            record = record._replace(polling_place_uprn="10001329795")
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
