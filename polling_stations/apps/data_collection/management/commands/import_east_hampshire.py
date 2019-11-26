from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000085"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019EHDC.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019EHDC.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def get_station_hash(self, record):
        return "-".join(
            [record.polling_place_id, record.polling_place_district_reference]
        )

    def station_record_to_dict(self, record):
        # corrections: https://trello.com/c/OGsqpfn4
        # we can't use the station ref here
        # because it also serves another district
        if record.polling_place_district_reference == "AL":
            record = record._replace(
                # replace the ID here so we don't end up with 2 different
                # station addresses for station ID 11829
                polling_place_id="AL",
                polling_place_name="The Wickham Institute",
                polling_place_address_1="Church Street",
                polling_place_address_2="Binsted",
                polling_place_address_3="Hampshire",
                polling_place_address_4="",
                polling_place_postcode="GU34 4NX",
                polling_place_easting="",
                polling_place_northing="",
            )

        if record.polling_place_id == "11806":
            record = record._replace(
                polling_place_name="Alton Community Centre",
                polling_place_address_1="Amery Street",
                polling_place_address_2="Alton",
                polling_place_address_3="Hampshire",
                polling_place_address_4="",
                polling_place_postcode="GU34 1HN",
                polling_place_easting="",
                polling_place_northing="",
            )

        # Jubilee Hall, Crouch Lane
        rec = super().station_record_to_dict(record)
        if record.polling_place_id == "11962":
            rec["location"] = Point(-1.013446, 50.916221, srid=4326)

        return rec

    def address_record_to_dict(self, record):

        # ...and make the corresponding change when importing the addresses
        # so that the station ids match up
        if record.polling_place_district_reference == "AL":
            record = record._replace(polling_place_id="AL")

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10009815841":
            rec["postcode"] = "GU10 5JL"

        if uprn in [
            "10032904465",  # GU307QL -> GU307GL : 5 Cavendish House, 3/4, Tudor Court, Liphook, Hants
            "100060267079",  # GU345LT -> GU345NN : Trinity Farm, Trinity Hill, Medstead, Alton, Hants
            "10090973748",  # GU336LE -> GU336LA : West Fork Place, Farnham Road, West Liss, Liss, Hants
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10009815781",  # GU344ND -> GU344NE : The Lodge, Coldrey Farm, Lower Froyle, Alton, Hants
            "100060269031",  # GU358DS -> GU358DB : Newlands, Headley Hill Road, Headley Down, Bordon, Hants
            "100062342567",  # GU307RN -> GU307RX : 2 The Oast Houses, Headley Lane, Passfield, Liphook, Hants
            "1710006656",  # GU345BJ -> GU345FX : Oakdene, 2 handyside place, The Shrave, Four Marks, Alton, Hants
            "1710049581",  # GU350QB -> GU350QL : 27 Grayshott Laurels, Lindford, Bordon, Hants
            "100062321534",  # GU102QG -> GU102QE : Kingsmead, Frensham Lane, Churt, Farnham, Surrey
        ]:
            rec["accept_suggestion"] = False

        return rec
