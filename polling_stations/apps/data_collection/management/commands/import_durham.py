from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000047"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019dur.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019dur.CSV"
    elections = ["parl.2019-12-12"]
    csv_delimiter = ","
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10000806992":
            rec["postcode"] = "DH8 9UN"

        if uprn in [
            "100110501314",
            "10014556896",
            "100110519859",
            "10094408615",
            "200002972415",
        ]:
            return None

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "46013":
            record = record._replace(polling_place_postcode="")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)
