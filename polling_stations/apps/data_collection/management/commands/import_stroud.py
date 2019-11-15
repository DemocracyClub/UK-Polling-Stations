from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000082"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100120528842",
            "10092977212",
            "10092978161",
        ]:
            return None

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "16472":  # Arthur S Winterbotham Memorial Hall
            record = record._replace(polling_place_easting="374915")
            record = record._replace(polling_place_northing="200440")

        if record.polling_place_id == "16476":  # Bussage Village Hall
            record = record._replace(polling_place_postcode="GL68BB")
            record = record._replace(polling_place_easting="388393")
            record = record._replace(polling_place_northing="203373")

        return super().station_record_to_dict(record)
