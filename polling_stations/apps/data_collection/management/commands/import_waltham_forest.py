from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000031"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # better point for Mission Grove South Site
        if record.polling_place_id == "4202":
            rec["location"] = Point(-0.025035, 51.581813, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10024419155":
            rec["postcode"] = "E179AY"
            rec["accept_suggestion"] = False

        if record.addressline6.strip() == "E17 5FX":
            return None

        if uprn in [
            "10009150015",  # E105EQ -> E105DR : 113A Vicarage Road, London
            "10091187735",  # E174ED -> E114ED : Flat 2, 147 Grove Green Road, London
            "10093562933",  # E173DA -> E177DA : 33 Storey Road, London
            "10093560515",  # E179NH -> E176NH : Flat H, 158 Blackhorse Road, London
            "200001427780",  # E174PE -> E177PE : Ground Floor, 70-72 St. James Street, London
            "10091185796",  # E177EA -> E107EA : First & Second Floor Flat 2, 403 Lea Bridge Road, London
            "100022958302",  # E107LN -> E107NE : 221A Lea Bridge Road, London
            "10091185806",  # E103BD -> E173BD : 61H Church Hill, London
            "200001431268",  # E177PB -> E177PJ : 6A St. James Mews, London
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200001414968",  # E106EF -> E106EE : First Floor Flat 2, 89 Canterbury Road, London
            "100022549240",  # E114EJ -> E113AN : 2A Grove Green Road, London
            "100022554291",  # E114HH -> E113HU : Ground Floor, 257 High Road Leytonstone, London
            "200001420368",  # E152BP -> E152BX : First Floor and Second Floor Flat, 96 High Road Leyton, London
        ]:
            rec["accept_suggestion"] = False

        return rec
