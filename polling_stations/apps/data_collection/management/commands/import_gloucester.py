from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000081"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019glouces.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019glouces.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # St Paul and St Stephen Church
        if record.polling_place_id == "3200":
            record = record._replace(polling_place_postcode="GL1 5AL")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.245029, 51.854501, srid=4326)
            return rec

        # St Lawrence Church Centre
        if record.polling_place_id == "3145":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.206526, 51.858234, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007318936",  # GL24DE -> GL45DE : 294 Painswick Road, Gloucester
            "10007318921",  # GL46JR -> GL46JB : 24B Bazeley Road, Gloucester
            "10007304835",  # GL13NP -> GL13NF : 1 Picton House, Wellington Parade, Gloucester
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10007317909",  # GL46LP -> GL46ES : 48A Birchall Avenue, Gloucester
            "10007319078",  # GL12NZ -> GL46PW : 78A Westgate Street, Gloucester
            "10007310053",  # GL15AL -> GL15AN : Flat 3, 6 Park End Road, Gloucester
            "100120469680",  # GL20JT -> GL12QL : 115 Elmleaze, Gloucester
            "100120474388",  # GL14PJ -> GL14PN : 13 Lattistep Court, Hatherley Road, Gloucester
            "100121248175",  # GL15PT -> GL15PX : 24B Seymour Road, Gloucester
        ]:
            rec["accept_suggestion"] = False

        return rec
