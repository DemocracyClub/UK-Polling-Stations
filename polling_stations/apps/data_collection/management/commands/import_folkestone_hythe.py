from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000112"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019folkstone.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019folkstone.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "50104978",  # TN299AU -> TN299UA : Headmasters House, Rhee Wall, Brenzett, Romney Marsh, Kent
            "50042070",  # CT202NQ -> CT202QN : Flat D, 104 Cheriton Road, Folkestone, Kent
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "50124993",  # CT195UW -> CT202PX : 1 Melanie Close, Folkestone, Kent
            "50124434",  # CT188LW -> CT188EW : Annexe Holly Lodge, Reece Lane, Acrise, Folkestone, Kent
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        uprns = {
            "5223": "50032257",  # Wards Hotel
            "5279": "50046311",  # St Marys Primary School
            "5283": "50102495",  # Hawkinge Community Centre
            "5342": "50103399",  # Newington Village Hall
            "5260": "50021990",  # Elham Village Hall
            "5264": "50011466",  # Bodsham Primary School
            "5245": "50011480",  # The Neptune
            "5364": "50103652",  # The Star Inn
            "5317": "50103844",  # Dungeness Lifeboat Station
            "5387": "50001094",  # Rose & Crown
        }

        gridrefs = {
            "5384": Point(1.0357008, 51.1383074, srid=4326),  # Peace Room
            "5323": Point(1.0842234, 51.1261431, srid=4326),  # Lyminge Village Hall
            "5214": Point(0.9963577, 51.048795, srid=4326),  # Burmarsh Church Hall
            "5198": Point(0.8502587, 51.0086578, srid=4326),  # Brenzett Village Hall
        }

        if record.polling_place_id == "5244":
            record = record._replace(polling_place_postcode="TN29 0NX")

        if record.polling_place_id in uprns:
            record = record._replace(polling_place_uprn=uprns[record.polling_place_id])
        rec = super().station_record_to_dict(record)
        if record.polling_place_id in gridrefs:
            rec["location"] = gridrefs[record.polling_place_id]

        return rec
