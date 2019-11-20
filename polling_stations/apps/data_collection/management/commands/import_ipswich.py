from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000202"
    addresses_name = "parl.2019-12-12/Version 2/ipswich.gov.uk-1573574354000-.CSV"
    stations_name = "parl.2019-12-12/Version 2/ipswich.gov.uk-1573574354000-.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # Sikh Temple
        if record.polling_place_id == "6642":
            record = record._replace(polling_place_uprn="10035058265")

        # Castle Hill United Reformed Church
        if record.polling_place_id == "6629":
            record = record._replace(polling_place_uprn="100091483837")

        # St Thomas the Apostle Church
        if record.polling_place_id == "6638":
            record = record._replace(
                polling_place_uprn="10004564181", polling_place_postcode="IP1 5BS"
            )

        # Stoke Green Baptist Church Hall
        if record.polling_place_id == "6827":
            record = record._replace(polling_place_uprn="10004567047")

        # Ascension Hall
        if record.polling_place_id == "6655":
            record = record._replace(polling_place_uprn="200001930783")

        # Broomhill Library
        if record.polling_place_id == "6659":
            record = record._replace(polling_place_uprn="10004565452")

        # St Mark`s RC Church Hall
        if record.polling_place_id == "6834":
            record = record._replace(polling_place_easting="614239")
            record = record._replace(polling_place_northing="243310")

        # Belstead Arms Public House
        if record.polling_place_id == "6863":
            record = record._replace(
                polling_place_uprn="10004566897", polling_place_postcode="IP2 9QU"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091636692",  # IP42AU -> IP42AT : 39 St Margarets Street, Ipswich
        ]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        # UPRNs not in addressbase
        if record.post_code in ["IP", "IP1", "IP2"]:
            return None

        if uprn in ["10093555944"]:
            return None

        return super().address_record_to_dict(record)
