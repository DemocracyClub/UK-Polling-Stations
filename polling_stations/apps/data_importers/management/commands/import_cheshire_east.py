from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHE"
    addresses_name = (
        "2023-05-04/2023-03-01T16:36:05.077147/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-01T16:36:05.077147/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001127574",  # THE SHEILING, DODDINGTON, NANTWICH
            "100012357368",  # MOSS FARM PARKERS ROAD, CREWE
            "10094310824",  # 1 CLIFF AUCOTT CRESCENT, ALSAGER, STOKE-ON-TRENT
            "10014451916",  # BRINDLEY FARM, WREXHAM ROAD, BURLAND, NANTWICH
            "10007953840",  # FOUR OAKS, THE COPPICE, POYNTON, STOCKPORT
            "10007965671",  # CROOKED YARD FARM, MACCLESFIELD FOREST, MACCLESFIELD
            "10007965347",  # THE BARN, CARR FIELD FARM, CHELFORD ROAD, ALDERLEY EDGE
            "10007956899",  # BRINK FARM COTTAGE, POTT SHRIGLEY, MACCLESFIELD
            "10007966889",  # BRINK FARM, POTT SHRIGLEY, MACCLESFIELD
            "100012771933",  # PYMCHAIR FARM, SALTERSFORD, RAINOW, MACCLESFIELD
            "100012358349",  # HALL O'COOLE, HEATLEY LANE, BROOMHALL, NANTWICH
            "100012367117",  # GOLDEN HILL FARM, WINCLE, MACCLESFIELD
            "10007965843",  # WARRILOWHEAD FARM, WALKER BARN, MACCLESFIELD
            "200000657078",  # CHAPEL HOUSE, HOLMES CHAPEL ROAD, DAVENPORT, CONGLETON
            "100012355389",  # BROOKFIELD HALL, DAVENPORT LANE, ARCLID, SANDBACH
        ]:
            return None

        if record.addressline6 in [
            # splits
            "WA16 0GU",
            "CW1 5BS",
            "WA16 0GQ",
            "WA16 0XQ",
            "SK10 3PG",
            "WA16 0XN",
            "CW4 7AG",
            "CW2 8LA",
            "SK12 1UB",
            "CW5 7HN",
            "CW12 2NA",
            "SK11 7ZG",
            "ST7 2ZN",
            "ST7 2ZT",
            "SK10 5LE",  # LIMEFIELD ESTATE STABLES LIME FIELD, BOLLINGTON
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Goodwill Hall Wrexham Road Faddiley Nantwich CW5 8HY
        if rec["internal_council_id"] == "3989":
            rec["location"] = Point(-2.611955, 53.074191, srid=4326)

        # Holy Trinity Church Hall, Community Hub, 197A Hurdsfield Road, Macclesfield
        if rec["internal_council_id"] == "3352":
            rec["location"] = Point(-2.112875, 53.264374, srid=4326)

        # Davenport Methodist Church, Holmes Chapel Road, Near Somerford
        if rec["internal_council_id"] == "3363":
            rec["location"] = Point(-2.297538, 53.184047, srid=4326)

        return rec
