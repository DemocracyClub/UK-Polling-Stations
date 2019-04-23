from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000031"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # better point for Mission Grove South Site
        # From previous script, but still improves
        if record.polling_place_id == "3878":
            rec["location"] = Point(-0.025035, 51.581813, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10093563415":
            rec["postcode"] = "E70AR"
            rec["accept_suggestion"] = False
        if uprn == "10024419155":
            rec["postcode"] = "E179AY"
            rec["accept_suggestion"] = False

        if uprn in [
            "10009150015",  # E105EQ -> E105DR : 113A Vicarage Road, London
            "10091187735",  # E174ED -> E114ED : Flat 2, 147 Grove Green Road, London
            "200001420373",  # E152BX -> E152DE : 100A High Road Leyton, London
            "10093562933",  # E173DA -> E177DA : 33 Storey Road, London
            "10093560515",  # E179NH -> E176NH : Flat H, 158 Blackhorse Road, London
            "200001427780",  # E174PE -> E177PE : Ground Floor, 70-72 St. James Street, London
            "10093560485",  # E179NZ -> E179DS : Flat 1, 859 Lea Bridge Road, London
            "10093560486",  # E179NZ -> E179DS : Flat 2, 859 Lea Bridge Road, London
            "10093560487",  # E179NZ -> E179DS : Flat 3, 859 Lea Bridge Road, London
            "10093560488",  # E179NZ -> E179DS : Flat 4, 859 Lea Bridge Road, London
            "10093560489",  # E179NZ -> E179DS : Flat 5, 859 Lea Bridge Road, London
            "10093560490",  # E179NZ -> E179DS : Flat 6, 859 Lea Bridge Road, London
            "10093560491",  # E179NZ -> E179DS : Flat 7, 859 Lea Bridge Road, London
            "10093560492",  # E179NZ -> E179DS : Flat 8, 859 Lea Bridge Road, London
            "10093560493",  # E179NZ -> E179DS : Flat 9, 859 Lea Bridge Road, London
            "10093560494",  # E179NZ -> E179DS : Flat 10, 859 Lea Bridge Road, London
            "10093560495",  # E179NZ -> E179DS : Flat 11, 859 Lea Bridge Road, London
            "10093560496",  # E179NZ -> E179DS : Flat 12, 859 Lea Bridge Road, London
            "10091185796",  # E177EA -> E107EA : First & Second Floor Flat 2, 403 Lea Bridge Road, London
            "100022958302",  # E107LN -> E107NE : 221A Lea Bridge Road, London
            "10091185806",  # E103BD -> E173BD : 61H Church Hill, London
            "10093560497",  # E179NZ -> E179DS : Flat 13, 859 Lea Bridge Road, London
            "10093560498",  # E179NZ -> E179DS : Flat 14, 859 Lea Bridge Road, London
            "10093560499",  # E179NZ -> E179DS : Flat 15, 859 Lea Bridge Road, London
            "10093560500",  # E179NZ -> E179DS : Flat 16, 859 Lea Bridge Road, London
            "10093560501",  # E179NZ -> E179DS : Flat 17, 859 Lea Bridge Road, London
            "10093560502",  # E179NZ -> E179DS : Flat 18, 859 Lea Bridge Road, London
            "10093560503",  # E179NZ -> E179DS : Flat 19, 859 Lea Bridge Road, London
            "10093560504",  # E179NZ -> E179DS : Flat 20, 859 Lea Bridge Road, London
            "10093560505",  # E179NZ -> E179DS : Flat 21, 859 Lea Bridge Road, London
            "10093560506",  # E179NZ -> E179DS : Flat 22, 859 Lea Bridge Road, London
            "10093560507",  # E179NZ -> E179DS : Flat 23, 859 Lea Bridge Road, London
            "200001431268",  # E177PB -> E177PJ : 6A St. James Mews, London
            "10093561445",  # E177FL -> E177AS : 1 Manby Walk, London
            "10093561446",  # E177FL -> E177AS : 2 Manby Walk, London
            "10093561447",  # E177FL -> E177AS : 3 Manby Walk, London
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200001414968",  # E106EF -> E106EE : First Floor Flat 2, 89 Canterbury Road, London
            "10009149280",  # E113HS -> E105PW : First Floor Flat Rear, 304A High Road Leytonstone, London
            "10009149281",  # E113HS -> E105PW : First Floor Flat Front, 304A High Road Leytonstone, London
            "100022549240",  # E114EJ -> E113AN : 2A Grove Green Road, London
            "100022554291",  # E114HH -> E113HU : Ground Floor, 257 High Road Leytonstone, London
            "200001420368",  # E152BP -> E152BX : First Floor and Second Floor Flat, 96 High Road Leyton, London
        ]:
            rec["accept_suggestion"] = False

        return rec
