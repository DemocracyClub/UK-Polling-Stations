from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000037"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Wberks.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Wberks.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Leckhampstead Village Hall
        if record.polling_place_id == "3915":
            record = record._replace(polling_place_postcode="RG20 8QZ")

        rec = super().station_record_to_dict(record)

        # Holybrook Centre
        if record.polling_place_id == "4135":
            rec["location"] = Point(-1.025829, 51.441617, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004724874",  # RG317RS -> RG317RJ : Latymer House, The Spinney, Mill Lane, Calcot, Reading, Berks
            "200004722978",  # RG88JN -> RG88SN : Clayhanger Farm, Whitemoor Lane, Upper Basildon, Reading, Berks
            "10022808688",  # RG76LE -> RG76LT : The Old Boot Inn, Stanford Dingley, Reading, Berks
            "10023922811",  # RG179SX -> RG179QT : Little Barn, Owls Barn, Rooksnest Lane, Kintbury, Hungerford, Berks
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200001659934",  # RG88ES -> RG88ER : The Tithe Barn, Tidmarsh, Reading, Berks
            "200004736141",  # RG75TS -> RG75UA : Lindens, Carbinswood Lane, Upper Woolhampton, Reading, Berks
            "200002099786",  # RG189SB -> RG189SD : West Barn, Manor Farm, Oare, Hermitage, Thatcham, Berks
            "200004734381",  # RG143BL -> RG143BP : Bussock Mayne, Snelsmore Common, Winterbourne, Newbury, Berks
            "10009203203",  # RG141RH -> RG208EP : Gateway Cottage, Bath Road, Speen, Newbury, Berks
            "10009201431",  # RG143BG -> RG143BH : West Lodge, Snelsmore Common, Newbury, Berks
            "10009199275",  # OX129NL -> OX129NN : Littleworth Farmhouse, South Fawley, Wantage, Oxon
            "10009200802",  # RG208SU -> RG208TU : Mobile Home, Old Street, Beedon, Newbury, Berks
            "100081023961",  # RG73JS -> RG73ZF : Bay Tree Cottage, Hollybush Lane, Burghfield Common, Reading, Berks
            "10023920503",  # RG189SB -> RG170YU : Caravan, Stable View, Manor Lane, Oare, Newbury, Berks
            "10023920214",  # RG88PU -> RG88JG : Bowdenside Farm Nurseries, Yattendon Road, Pangbourne, Reading, Berks
            "200004735176",  # RG88JJ -> RG88PT : Bowden Corner, Yattendon Road, Pangbourne, Reading, Berks
            "10022809953",  # RG88JJ -> RG88PT : Tysoe Farm, Yattendon Road, Pangbourne, Reading, Berks
            "200004723705",  # RG75ES -> RG75ER : Old School House, The Street, Englefield, Reading, Berks
        ]:
            rec["accept_suggestion"] = False

        return rec
