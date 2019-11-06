from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000112"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019 F&H.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019 F&H.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "50102150":
            rec["postcode"] = "CT20 2EF"
            rec["accept_suggestion"] = False

        if uprn in [
            "50104978",  # TN299AU -> TN299UA : Headmasters House, Rhee Wall, Brenzett, Romney Marsh, Kent
            "50042070",  # CT202NQ -> CT202QN : Flat D, 104 Cheriton Road, Folkestone, Kent
        ]:
            rec["accept_suggestion"] = True

        return rec

    def station_record_to_dict(self, record):
        uprns = {
            "6299": "50032257",  # Wards Hotel
            "6291": "50046311",  # St Marys Primary School
            "6212": "50102495",  # Hawkinge Community Centre
            "6226": "50103399",  # Newington Village Hall
            "6197": "50021990",  # Elham Village Hall
            "6245": "50011466",  # Bodsham Primary School
            "6366": "50011480",  # The Neptune
            "6394": "50103652",  # The Star Inn
            "6391": "50001094",  # Rose & Crown
        }

        gridrefs = {
            "6251": Point(1.0357008, 51.1383074, srid=4326),  # Peace Room
            "6373": Point(0.9963577, 51.048795, srid=4326),  # Burmarsh Church Hall
            "6376": Point(0.8502587, 51.0086578, srid=4326),  # Brenzett Village Hall
            "6319": Point(1.119211, 51.072634, srid=4326),  # The Fountain Pub
        }

        """
        Email

        Please note that WDM5 – Ivychurch Parish has had a last minute change
        of polling station, it is now:
        St Georges Church, Ashford Road, Ivychurch, Romney Marsh, TN29 0AL
        Can you please update accordingly. Thanks in adv.
        """
        if record.polling_place_id == "6383":
            record = record._replace(polling_place_name="St Georges Church")
            record = record._replace(polling_place_address_1="Ashford Road")
            record = record._replace(polling_place_address_2="Ivychurch")
            record = record._replace(polling_place_address_3="Romney Marsh")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="TN29 0AL")
            record = record._replace(polling_place_uprn="")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        # Correction via email
        if record.polling_place_id == "6400":
            record = record._replace(polling_place_postcode="TN29 0NX")

        if record.polling_place_id in uprns:
            record = record._replace(polling_place_uprn=uprns[record.polling_place_id])

        rec = super().station_record_to_dict(record)

        if record.polling_place_id in gridrefs:
            rec["location"] = gridrefs[record.polling_place_id]

        return rec
