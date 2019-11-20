from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000203"
    addresses_name = "parl.2019-12-12/Version 1/MSDCDemocracy_Club__07May2020.CSV"
    stations_name = "parl.2019-12-12/Version 1/MSDCDemocracy_Club__07May2020.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10090893715":
            rec["postcode"] = "IP6 8HJ"
            rec["accept_suggestion"] = False

        if uprn == "100091375182":
            rec["postcode"] = "IP30 9PE"
            rec["accept_suggestion"] = False

        if uprn == "10090890000":
            rec["postcode"] = "IP6 0EP"
            rec["accept_suggestion"] = False

        if uprn == "100091382079":
            return None

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "17450":
            record = record._replace(polling_place_postcode="IP20 0JE")
            record = record._replace(polling_place_easting="627286.25")
            record = record._replace(polling_place_northing="281055.48")

        # recieved from council
        if record.polling_place_id == "17440":  # Kenton - Caravan near former Station
            record = record._replace(
                polling_place_name="Bedingfield Village Hall",
                polling_place_address_1="Church Corner",
                polling_place_address_2="Bedingfield",
                polling_place_postcode="IP23 7QG",
            )
        if record.polling_place_id == "17355":  # Elmswell (ELS) - The Wesley
            record = record._replace(
                polling_place_name="Elmswell (ELN) - Blackbourne Centre",
                polling_place_address_1="Blackbourne Road",
                polling_place_address_2="Elmswell",
                polling_place_postcode="IP30 9UH",
            )
        return super().station_record_to_dict(record)
