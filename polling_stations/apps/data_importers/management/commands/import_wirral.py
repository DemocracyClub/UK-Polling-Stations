from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRL"
    addresses_name = "2024-07-04/2024-06-24T15:10:49.934026/WRL_combined.tsv"
    stations_name = "2024-07-04/2024-06-24T15:10:49.934026/WRL_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # point correction for: Marlowe Road URC Hall (Station A and B), Marlowe Road, Wallasey, Wirral, CH44 3DG
        if record.polling_place_id in ["11911", "11913"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.050648, 53.417306, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "42127372",  # MANAGERS FLAT HALFWAY HOUSE 293 WOODCHURCH ROAD, PRENTON
                "42004030",  # GREEN COTTAGE, ARROWE PARK ROAD, WIRRAL
                "42194110",  # CHARTWELL GAYTON STABLES CHESTER ROAD, GAYTON
                "42205031",  # 227A HOYLAKE ROAD, WIRRAL
                "42177133",  # LOVELL PARTNERSHIP LTD, MARKETING SUITE 497 BOROUGH ROAD, OXTON
                "42068483",  # 4 LORNE ROAD, PRENTON
                "42205588",  # 105 GROVE ROAD, WALLASEY
                "42005155",  # TOP FLOOR FLAT 9 ATHERTON STREET, NEW BRIGHTON
                "42192662",  # FRANKBY HALL FRANKBY CEMETERY MONTGOMERY HILL, FRANKBY
                "42193468",  # 84B WOODCHURCH LANE, BIRKENHEAD
                "42127048",  # 84C WOODCHURCH LANE, BIRKENHEAD
                "42198034",  # FLAT 6, 90 WOODCHURCH LANE, BIRKENHEAD
                "42111190",  # 177 STORETON ROAD, BIRKENHEAD
                "42181675",  # 467A OLD CHESTER ROAD, ROCK FERRY
                "42181676",  # 469A OLD CHESTER ROAD, ROCK FERRY
                "42202763",  # 62A WHITFIELD LANE, WIRRAL
                "42004032",  # MANAGERS FLAT ARROWE PARK HOTEL ARROWE PARK ROAD, WOODCHURCH
                "42204289",  # FLAT 2, 43 OLD BIDSTON ROAD, BIRKENHEAD
                "42204290",  # FLAT 3, 43 OLD BIDSTON ROAD, BIRKENHEAD
                "42204288",  # FLAT 1 43 OLD BIDSTON ROAD, BIRKENHEAD
                "42205131",  # 3 ST. JAMES ROAD, PRENTON
                "42205130",  # 1 ST. JAMES ROAD, PRENTON
                "42086861",  # FLAT, BIRKENHEAD PARK CRICKET CLUB, PARK DRIVE, PRENTON
                "42013858",  # 1004 BOROUGH ROAD, BIRKENHEAD
                "42202241",  # 15 MILL ROAD, BROMBOROUGH, WIRRAL
                "42016031",  # 63 BRIDLE ROAD, EASTHAM, WIRRAL
                "42159174",  # IVY COTTAGE, BRIMSTAGE LANE, WIRRAL
                "42076476",  # CALDY COTTAGE, MONTGOMERY HILL, WIRRAL
                "42195941",  # 102A MARKET STREET, HOYLAKE
                "42119290",  # HILLSIDE, UPTON ROAD, PRENTON
                "42168826",  # FLAT 5, 44 FOREST ROAD, PRENTON
                "42200980",  # LIVING ACCOMODATION 23-25 BALLS ROAD, OXTON
                "42155399",  # 2 ROCK COTTAGE, ROCK PARK ROAD, BIRKENHEAD
                "42002076",  # 89 ALLPORT LANE, WIRRAL
                "42198409",  # 15A NORTH PARADE, HOYLAKE, WIRRAL
                "42204322",  # 5 TAPLOW WAY, WIRRAL
                "42204323",  # 6 TAPLOW WAY, WIRRAL
                "42204324",  # 7 TAPLOW WAY, WIRRAL
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "CH49 2SE",
            "CH49 3PG",
            "CH62 8AB",
            # wrong
            "CH41 4BY",
            "CH46 8AE",
            "CH46 8AN",
        ]:
            return None

        return super().address_record_to_dict(record)
