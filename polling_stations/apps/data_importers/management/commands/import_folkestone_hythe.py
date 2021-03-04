from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHE"
    addresses_name = "2021-02-10T16:39:37.576273/Democracy_Club__06May2021.tsv"
    stations_name = "2021-02-10T16:39:37.576273/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in ["CT20 3RE", "TN29 9AU"]:
            return None
        if uprn == "50124434":
            return None
        return rec

    def station_record_to_dict(self, record):
        uprns = {
            "6872": "50032257",  # Wards Hotel
            "6888": "50102495",  # Hawkinge Community Centre
            "6899": "50103399",  # Newington Village Hall
            "6876": "50021990",  # Elham Village Hall
            "6922": "50011466",  # Bodsham Primary School
            "7008": "50011480",  # The Neptune
            "7056": "50103652",  # The Star Inn
            "7053": "50001094",  # Rose & Crown
        }

        gridrefs = {
            "6928": Point(1.0357008, 51.1383074, srid=4326),  # Peace Room
            "7036": Point(0.9963577, 51.048795, srid=4326),  # Burmarsh Church Hall
            "7039": Point(0.8502587, 51.0086578, srid=4326),  # Brenzett Village Hall
            "6862": Point(1.119211, 51.072634, srid=4326),  # The Fountain Pub
        }

        if record.polling_place_id in uprns:
            record = record._replace(polling_place_uprn=uprns[record.polling_place_id])

        rec = super().station_record_to_dict(record)

        if record.polling_place_id in gridrefs:
            rec["location"] = gridrefs[record.polling_place_id]

        return rec
