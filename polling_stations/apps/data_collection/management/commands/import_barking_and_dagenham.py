from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000002"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # Barking United Reform Church
        if record.polling_place_id == "6050":
            record = record._replace(polling_place_postcode="IG11 9LT")
            record = record._replace(polling_place_easting="545510")
            record = record._replace(polling_place_northing="184596")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if record.addressline6.strip() in [
            "RM9 5DX",
            "RM8 1DR",
            "RM9 6YD",
            "RM9 6XG",
            "RM9 6XH",
        ]:
            return None

        if uprn == "100012133":
            rec["postcode"] = "RM8 1DJ"
            rec["accept_suggestion"] = False

        if uprn in [
            "100041457",  # RM108BX -> RM109BX : 17 Dunchurch House, Ford Road, Dagenham, Essex
            "100033020",  # RM81BJ -> RM66RJ : 464A Whalebone Lane North, Chadwell Heath, Romford, Essex
        ]:
            rec["accept_suggestion"] = True

        return rec
