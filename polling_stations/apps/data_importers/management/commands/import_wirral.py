from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRL"
    addresses_name = "2021-03-25T18:36:07.708279/wirral_deduped.tsv"
    stations_name = "2021-03-25T18:36:07.708279/wirral_deduped.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Marlowe Road URC Hall
        if record.polling_place_id in ["7516", "7513"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.050648, 53.417306, srid=4326)
            return rec

        # user issue report #87
        # The Grange Public House
        if record.polling_place_id == "7536":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.122875, 53.396797, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "42194110",  # CHARTWELL GAYTON STABLES CHESTER ROAD, GAYTON
            "42007082",  # 103B BARNSTON ROAD, HESWALL, WIRRAL
            "42197144",  # 38A FENDER WAY, PRENTON
            "42192662",  # FRANKBY HALL FRANKBY CEMETERY MONTGOMERY HILL, FRANKBY
            "42193157",  # THE HAYLOFT, FRANKBY ROAD, FRANKBY, WIRRAL
            "42198324",  # 1 MANOR FARM BARN FRANKBY ROAD, FRANKBY
            "42198325",  # 2 MANOR FARM BARN FRANKBY ROAD, FRANKBY
            "42193209",  # THE BARN, FRANKBY ROAD, FRANKBY, WIRRAL
            "42005428",  # GROUND FLOOR FLAT 41 AVONDALE ROAD, HOYLAKE
            "42005429",  # FIRST FLOOR FLAT 41 AVONDALE ROAD, HOYLAKE
            "42195941",  # 102A MARKET STREET, HOYLAKE
            "42003905",  # 21A ARROWE PARK ROAD, WIRRAL
            "42198028",  # 21 BURDEN ROAD, MORETON
            "42135668",  # WAGNER DEVELOPMENTS LIMITED, 30 DINSDALE ROAD, BROMBOROUGH
            "42199810",  # FLAT 9, MERSEY GARDENS, OLD CHESTER ROAD, BIRKENHEAD
            "42192936",  # FLAT 3 55-57 OLD CHESTER ROAD, TRANMERE
            "42199950",  # BEDSIT 3 181 OLD CHESTER ROAD, TRANMERE
            "42199948",  # BEDSIT 1 181 OLD CHESTER ROAD, TRANMERE
            "42199951",  # BEDSIT 4 181 OLD CHESTER ROAD, TRANMERE
            "42199949",  # BEDSIT 2 181 OLD CHESTER ROAD, TRANMERE
            "42200745",  # BEDSIT 2 120 WOODCHURCH LANE, PRENTON
            "42200748",  # BEDSIT 5 120 WOODCHURCH LANE, PRENTON
            "42200747",  # BEDSIT 4 120 WOODCHURCH LANE, PRENTON
            "42200746",  # BEDSIT 3 120 WOODCHURCH LANE, PRENTON
            "42200744",  # BEDSIT 1 120 WOODCHURCH LANE, PRENTON
            "42193468",  # 84B WOODCHURCH LANE, BIRKENHEAD
            "42127048",  # 84C WOODCHURCH LANE, BIRKENHEAD
            "42198034",  # FLAT 6, 90 WOODCHURCH LANE, BIRKENHEAD
            "42179121",  # 42 CLIFTON ROAD, TRANMERE
            "42179120",  # 41 CLIFTON ROAD, BIRKENHEAD
            "42196854",  # BEDSIT 5 33 CLIFTON ROAD, TRANMERE
            "42196852",  # BEDSIT 3 33 CLIFTON ROAD, TRANMERE
            "42196850",  # BEDSIT 1 33 CLIFTON ROAD, TRANMERE
            "42203083",  # BASEMENT FLAT 33 CLIFTON ROAD, TRANMERE
            "42196853",  # BEDSIT 4 33 CLIFTON ROAD, TRANMERE
            "42026498",  # 33 CLIFTON ROAD, BIRKENHEAD
            "42196851",  # BEDSIT 2 33 CLIFTON ROAD, TRANMERE
            "42196855",  # BEDSIT 6 33 CLIFTON ROAD, TRANMERE
            "42200795",  # BEDSIT 4 3 CLIFTON ROAD, TRANMERE
            "42200794",  # BEDSIT 3 3 CLIFTON ROAD, TRANMERE
            "42200793",  # BEDSIT 2 3 CLIFTON ROAD, TRANMERE
            "42200796",  # BEDSIT 5 3 CLIFTON ROAD, TRANMERE
            "42200792",  # BEDSIT 1 3 CLIFTON ROAD, TRANMERE
            "42200833",  # BEDSIT 4 5 CLIFTON ROAD, TRANMERE
            "42200832",  # BEDSIT 3 5 CLIFTON ROAD, TRANMERE
            "42200831",  # BEDSIT 2 5 CLIFTON ROAD, TRANMERE
            "42200834",  # BEDSIT 5 5 CLIFTON ROAD, TRANMERE
            "42200830",  # BEDSIT 1 5 CLIFTON ROAD, TRANMERE
            "42005155",  # TOP FLOOR FLAT 9 ATHERTON STREET, NEW BRIGHTON
            "42193092",  # 11 GRANGE ROAD WEST, BIRKENHEAD
        ]:
            return None

        if record.addressline6 in ["CH62 8AB", "CH49 2SE", "CH49 3PG", "CH60 8QH"]:
            return None

        return super().address_record_to_dict(record)
