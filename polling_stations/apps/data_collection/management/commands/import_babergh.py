from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000200"
    addresses_name = "parl.2019-12-12/Version 1/BDCDemocracy_Club__07May2020.CSV"
    stations_name = "parl.2019-12-12/Version 1/BDCDemocracy_Club__07May2020.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10093346518":
            rec["postcode"] = "CO10 0JT"
            rec["accept_suggestion"] = False

        if uprn in ["10093346305", "10093346306"]:
            rec["postcode"] = "CO10 0BA"
            rec["accept_suggestion"] = False

        # Following addresses throw
        # 'Postcode centroid is outside target local authoritys' Warning
        # But can't find in AddressBase:
        # 'Bumbles, Hartest Road, Brockley, Bury St Edmunds'
        # 'Bumblebee Barn, Mill Street, Polstead, Colchester'
        if record.addressline1.startswith("Bumble"):
            return None

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "18388":
            record = record._replace(polling_place_easting="614333.04")
            record = record._replace(polling_place_northing="242066.66")

        # recieved from council
        if record.polling_place_id == "18250":  # Chilton - The White Horse Inn
            record = record._replace(
                polling_place_name="Great Waldingfield Village Hall",
                polling_place_address_1="The Heath",
                polling_place_address_2="Great Waldingfield",
                polling_place_postcode="CO10 0SE",
            )
        if record.polling_place_id == "18318":  # Harkstead Village Hall
            record = record._replace(
                polling_place_name="Holbrook Village Hall",
                polling_place_address_1="The Street",
                polling_place_address_2="Holbrook",
                polling_place_postcode="IP9 2PZ",
            )
        # https://trello.com/c/kKKWpgrl
        if record.polling_place_id == "18262":  # Pot Kiln School
            record = record._replace(
                polling_place_name="The Stevenson Centre",
                polling_place_address_1="Stevenson Approach",
                polling_place_address_2="Great Cornard",
                polling_place_address_3="Sudbury",
                polling_place_postcode="CO10 0WD",
            )

        return super().station_record_to_dict(record)
