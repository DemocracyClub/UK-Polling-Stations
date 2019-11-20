from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000181"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        if record.polling_place_id == "6700":
            record = record._replace(polling_place_postcode="OX18 3PU")
            record = record._replace(polling_place_easting="430059")
            record = record._replace(polling_place_northing="207340")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        # Annexe At Laurel Mount, 4 North Street, Middle Barton, Chipping Norton, Oxon
        if uprn == "10094864970":
            rec["postcode"] = "OX7 7BJ"
            rec["accept_suggestion"] = False

        if uprn == "10093355324":  # Annexe, 44 Green Lane, Woodstock, Oxon
            rec["postcode"] = "OX20 1JZ"
            rec["accept_suggestion"] = False

        if uprn in [
            "10033224093",  # Brew House Cottage, Chastleton, Moreton In Marsh, Glos GL56 0SU
            "10003998051",  # Stable Flat Heythrop Hunt Kennels, Kennels Lane, Heythrop, Chipping Norton, Ooxn  OX75YE
        ]:
            return None
        if uprn == "100120970053":
            rec["postcode"] = "GL7 3JH"

        if uprn == "200002436593":
            rec["postcode"] = "OX29 9UH"

        if record.addressline1.strip() == "Horseshoe Island":
            return None

        if uprn in [
            "10033228325",  # OX183HA -> OX182HA : The Horseshoe, Bridge Street, Bampton, Oxon
            "10002188547",  # OX183HW -> OX182HW : The Orchard, Weald Street, Weald, Bampton, Oxon
        ]:
            rec["accept_suggestion"] = True

        return rec
