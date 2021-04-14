from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "BIR"
    addresses_name = "2021-03-25T14:58:14.891168/polling_station_export-2021-03-24.csv"
    stations_name = "2021-03-25T14:58:14.891168/polling_station_export-2021-03-24.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if record.pollingstationname == "St Mary and Ambrose Church Hall":
            rec["postcode"] = "B5 7RA"
            rec["location"] = Point(-1.904365, 52.458623, srid=4326)

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100070582046",  # 6 CHURCHILL ROAD, SUTTON COLDFIELD
            "100070582044",  # 4 CHURCHILL ROAD, SUTTON COLDFIELD
            "100070582042",  # 2 CHURCHILL ROAD, SUTTON COLDFIELD
            "100070582048",  # 8 CHURCHILL ROAD, SUTTON COLDFIELD
            "100071313970",  # FLAT 10, 61 WARWICK ROAD, SUTTON COLDFIELD
            "100071313972",  # FLAT 12, 61 WARWICK ROAD, SUTTON COLDFIELD
            "100071313971",  # FLAT 11, 61 WARWICK ROAD, SUTTON COLDFIELD
            "10024263932",  # 4 HILLHURST ROAD, SUTTON COLDFIELD
            "10024263933",  # 6 HILLHURST ROAD, SUTTON COLDFIELD
            "10024263940",  # 18 HILLHURST ROAD, SUTTON COLDFIELD
            "10024263939",  # 16 HILLHURST ROAD, SUTTON COLDFIELD
            "10024263937",  # 14 HILLHURST ROAD, SUTTON COLDFIELD
            "10024263936",  # 12 HILLHURST ROAD, SUTTON COLDFIELD
            "10024263935",  # 10 HILLHURST ROAD, SUTTON COLDFIELD
            "10024263934",  # 8 HILLHURST ROAD, SUTTON COLDFIELD
            "100071441677",  # ST. EDMUND CAMPION RC SCHOOL, SUTTON ROAD, BIRMINGHAM
            "100071312419",  # FLAT 263 KINGSBURY ROAD, SUTTON NEW HALL, SUTTON COLDFIELD
            "10024448607",  # 71 PAGET ROAD, BIRMINGHAM
            "10023294692",  # FLAT 2 37 FRANCIS ROAD, STECHFORD AND YARDLEY NORTH, BIRMINGHAM
            "10023294690",  # FLAT 1 37 FRANCIS ROAD, STECHFORD AND YARDLEY NORTH, BIRMINGHAM
            "10023294691",  # FLAT 3 37 FRANCIS ROAD, STECHFORD AND YARDLEY NORTH, BIRMINGHAM
            "10024263239",  # CARETAKERS HOUSE, 250 WASH LANE, BIRMINGHAM
            "100070392402",  # 285 HAMSTEAD ROAD, HANDSWORTH, BIRMINGHAM
            "100070392400",  # 283 HAMSTEAD ROAD, HANDSWORTH, BIRMINGHAM
            "10023295371",  # 10A GROSVENOR ROAD, QUINTON, BIRMINGHAM
            "100070535261",  # 230 THE BROADWAY, BIRMINGHAM
            "10090246839",  # FLAT 3 462 MOSELEY ROAD, SPARKBROOK, BIRMINGHAM
            "10094293202",  # 17 MARY STREET, BIRMINGHAM
            "100070414537",  # 5 ICKNIELD PORT ROAD, BIRMINGHAM
            "100070414536",  # 4 ICKNIELD PORT ROAD, BIRMINGHAM
            "100070414535",  # 3 ICKNIELD PORT ROAD, BIRMINGHAM
            "100070414534",  # 2 ICKNIELD PORT ROAD, BIRMINGHAM
            "100070414533",  # 1 ICKNIELD PORT ROAD, BIRMINGHAM
            "100070325182",  # 7 CHURCH AVENUE, ST. MARYS ROW, MOSELEY, BIRMINGHAM
            "100071294188",  # HAZELWELL, PINEAPPLE ROAD, BIRMINGHAM
            "10093329745",  # 70C MIDDLETON HALL ROAD, BIRMINGHAM
            "10093329744",  # 70B MIDDLETON HALL ROAD, BIRMINGHAM
            "10023506544",  # 27 REA ROAD, NORTHFIELD, BIRMINGHAM
            "10023506545",  # 29 REA ROAD, NORTHFIELD, BIRMINGHAM
            "10023506546",  # 31 REA ROAD, NORTHFIELD, BIRMINGHAM
            "10023506547",  # 33 REA ROAD, NORTHFIELD, BIRMINGHAM
            "100070471109",  # 67A OSBORN ROAD, BIRMINGHAM
            "10093329674",  # 35D OLTON BOULEVARD EAST, BIRMINGHAM
            "100070549934",  # 10 LENCHS CLOSE, BIRMINGHAM
            "100070549936",  # 12 LENCHS CLOSE, BIRMINGHAM
            "100070549938",  # 14 LENCHS CLOSE, BIRMINGHAM
            "100070549940",  # 16 LENCHS CLOSE, BIRMINGHAM
            "100070549942",  # 18 LENCHS CLOSE, BIRMINGHAM
            "10090246839",  # FLAT 3 462 MOSELEY ROAD, SPARKBROOK, BIRMINGHAM
            "100071270260",  # FLAT 201 CHURCH ROAD, STECHFORD AND YARDLEY NORTH, BIRMINGHAM
            "100070578935",  # 119 BIRMINGHAM ROAD, SUTTON COLDFIELD
            "100070578936",  # 121 BIRMINGHAM ROAD, SUTTON COLDFIELD
            "100070578933",  # 117 BIRMINGHAM ROAD, SUTTON COLDFIELD
            "100071268408",  # FLAT 2, 7 CAVERSHAM ROAD, BIRMINGHAM
            "10033390956",  # FLAT 56A WASHWOOD HEATH ROAD, BIRMINGHAM
            "100071484540",  # 65 COLESHILL ROAD, SUTTON COLDFIELD
            "100071484542",  # 69 COLESHILL ROAD, SUTTON COLDFIELD
            "100070307615",  # 3 BROMFORD DRIVE, BIRMINGHAM
        ]:
            return None

        if record.housepostcode in [
            "B31 1AE",
            "B31 3JE",
            "B14 6LD",
            "B28 9QL",
            "B34 6NE",
            "B23 5AL",
            "B23 7XE",
            "B31 5NH",
            "B31 2FL",
            "B13 9UA",
            "B7 5LD",
            "B31 5BG",
            "B30 1TH",
            "B33 9QD",
            "B75 5NE",
            "B31 2AE",
            "B31 2AD",
            "B29 7ES",
            "B20 3QT",
            "B72 1DX",
            "B35 7LH",
            "B35 7NW",
            "B10 0BS",
        ]:
            return None

        return super().address_record_to_dict(record)
