from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000202"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Ipswich.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Ipswich.CSV"
    elections = ["local.2019-05-02"]

    def station_record_to_dict(self, record):

        # Sikh Temple
        if record.polling_place_id == "5454":
            record = record._replace(polling_place_uprn="10035058265")

        # Castle Hill United Reformed Church
        if record.polling_place_id == "5470":
            record = record._replace(polling_place_uprn="100091483837")

        # St Thomas the Apostle Church
        if record.polling_place_id == "5450":
            record = record._replace(polling_place_uprn="10004564181")

        # Stoke Green Baptist Church Hall
        if record.polling_place_id == "5293":
            record = record._replace(polling_place_uprn="10004567047")

        # Ascension Hall
        if record.polling_place_id == "5300":
            record = record._replace(polling_place_uprn="200001930783")

        # Broomhill Library
        if record.polling_place_id == "5304":
            record = record._replace(polling_place_uprn="10004565452")

        # Mobile Unit ID in bus turning circle
        if record.polling_place_id == "5428":
            record = record._replace(polling_place_easting="614330")
            record = record._replace(polling_place_northing="242435")

        # St Mark`s RC Church Hall
        if record.polling_place_id == "5327":
            record = record._replace(polling_place_easting="614239")
            record = record._replace(polling_place_northing="243310")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["100091636692", "10093555116", "100091482960"]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        return super().address_record_to_dict(record)
