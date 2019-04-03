from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000085"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019easthants.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019easthants.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        if record.polling_place_id == "10278":
            rec["location"] = Point(-1.013446, 50.916221, srid=4326)
        return rec

    def address_record_to_dict(self, record):
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
            "1710006647",  # GU345BJ -> GU345QQ : Assissi, The Shrave, Four Marks, Alton, Hants
            "100060269031",  # GU358DS -> GU358DB : Newlands, Headley Hill Road, Headley Down, Bordon, Hants
            "100060260403",  # GU344BS -> GU344FG : Cadnams Farm, Anstey Lane, Alton, Hants
            "100062342567",  # GU307RN -> GU307RX : 2 The Oast Houses, Headley Lane, Passfield, Liphook, Hants
            "1710007913",  # GU343ET -> GU343DE : Greenmore, Brightstone Lane, Lower Farringdon, Alton, Hants
            "1710006656",  # GU345BJ -> GU345FX : Oakdene, 2 handyside place, The Shrave, Four Marks, Alton, Hants
            "1710049581",  # GU350QB -> GU350QL : 27 Grayshott Laurels, Lindford, Bordon, Hants
            "100062321534",  # GU102QG -> GU102QE : Kingsmead, Frensham Lane, Churt, Farnham, Surrey
        ]:
            rec["accept_suggestion"] = False

        return rec
