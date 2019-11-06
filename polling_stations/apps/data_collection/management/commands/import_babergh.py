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

        return super().station_record_to_dict(record)
