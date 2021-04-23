from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COV"
    addresses_name = "2021-04-13T12:12:57.429911/Coventry_deduped.tsv"
    stations_name = "2021-04-13T12:12:57.429911/Coventry_deduped.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Community Centre Warwickshire Shopping Park Kynner Way Binley Coventry CV3 2BS
        if record.polling_place_id == "13766":
            record = record._replace(polling_place_postcode="CV3 2SB")

        # Parkgate Primary School Parkgate Road Coventry CV5 7LR
        if record.polling_place_id == "13490":
            record = record._replace(polling_place_postcode="CV6 4GF")

        # St. James Church Hall Westcotes Coventry CV4 9BD
        if record.polling_place_id == "13700":
            record = record._replace(polling_place_easting="429643")
            record = record._replace(polling_place_northing="278413")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091717520",  # 224 TORRINGTON AVENUE, COVENTRY
            "100071515845",  # 2A NEWCOMBE ROAD, COVENTRY
            "10094849274",  # FLAT 3 279 WALSGRAVE ROAD, COVENTRY
            "10094849275",  # FLAT 4 279 WALSGRAVE ROAD, COVENTRY
            "10094849273",  # FLAT 2 279 WALSGRAVE ROAD, COVENTRY
            "10093949639",  # FLAT 3 119 WALSGRAVE ROAD, COVENTRY
            "10093948773",  # GROUND FLOOR FLAT 119 WALSGRAVE ROAD, COVENTRY
            "10093948774",  # FIRST FLOOR FLAT 119 WALSGRAVE ROAD, COVENTRY
            "10091718353",  # 112 WOODWAY LANE, COVENTRY
            "10024028582",  # FLAT ABOVE THE WHEEL 624 SEWALL HIGHWAY, COVENTRY
            "10095510481",  # GROUND FLOOR FLAT 658 FOLESHILL ROAD, COVENTRY
            "10095510480",  # FIRST FLOOR FLAT 658 FOLESHILL ROAD, COVENTRY
            "10024030569",  # FLAT BUTTS RETREAT 126 BUTTS, COVENTRY
            "10094852182",  # ANNEXE 358 BROAD LANE, COVENTRY
            "10095509721",  # FLAT ABOVE BROAD LANE TRADING ESTATE BANNER LANE, COVENTRY
            "10095510461",  # GROUND FLOOR FLAT 230 HOLBROOK LANE, COVENTRY
            "10014006474",  # SCHOOL HOUSE WHITMORE PARK PRIMARY SCHOOL HALFORD LANE, COVENTRY
            "10023032376",  # GROUND FLOOR FLAT 280 CHEVERAL AVENUE, COVENTRY
            "10023032377",  # FIRST FLOOR FLAT 280 CHEVERAL AVENUE, COVENTRY
            "10095510454",  # GROUND FLOOR FLAT 2C KENPAS HIGHWAY, COVENTRY
            "10094853479",  # FLAT C 86 WALSGRAVE ROAD, COVENTRY
            "10014007628",  # WESTWOOD SOCIAL BUILDING UNIVERSITY OF WARWICK KIRBY CORNER ROAD, COVENTRY
        ]:
            return None

        if record.addressline6 in [
            "CV3 3FA",
            "CV3 1QH",
            "CV2 3FD",
            "CV2 1TA",
            "CV2 2XJ",
            "CV2 2XL",
            "CV6 7FA",
            "CV5 9NQ",
            "CV5 9NR",
            "CV7 8NJ",
            "CV2 1PX",
            "CV4 9LP",
            "CV4 9YJ",
            "CV2 1FX",
            "CV6 5NU",
            "CV1 4GZ",
        ]:
            return None

        return super().address_record_to_dict(record)
