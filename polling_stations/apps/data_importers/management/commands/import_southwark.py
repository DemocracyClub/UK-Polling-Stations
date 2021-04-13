from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWK"
    addresses_name = "2021-04-13T12:22:55.056323/southwark_deduped.tsv"
    stations_name = "2021-04-13T12:22:55.056323/southwark_deduped.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003422738",  # FLAT 2, 29 RODNEY PLACE, LONDON
            "200003422744",  # FLAT 8, 29 RODNEY PLACE, LONDON
            "200003422746",  # FLAT 10, 29 RODNEY PLACE, LONDON
            "200003422739",  # FLAT 3, 29 RODNEY PLACE, LONDON
            "200003422737",  # FLAT 1, 29 RODNEY PLACE, LONDON
            "200003422745",  # FLAT 9, 29 RODNEY PLACE, LONDON
            "200003422743",  # FLAT 7, 29 RODNEY PLACE, LONDON
            "200003422740",  # FLAT 4, 29 RODNEY PLACE, LONDON
            "200003422741",  # FLAT 5, 29 RODNEY PLACE, LONDON
            "200003422742",  # FLAT 6, 29 RODNEY PLACE, LONDON
            "200003380843",  # SHEET METAL MUSIC LTD, 212 ILDERTON ROAD, LONDON
            "10094086807",  # APARTMENT 1, 346 ROTHERHITHE STREET, LONDON
            "10093338854",  # 73C 73 CAMBERWELL GROVE, LONDON
            "10093338853",  # 73B 73 CAMBERWELL GROVE, LONDON
            "200003394858",  # 17 LYNDHURST WAY, LONDON
            "10094743403",  # 88 HALF MOON LANE, LONDON
            "10094743404",  # 90 HALF MOON LANE, LONDON
            "10094743401",  # 84 HALF MOON LANE, LONDON
            "10094743402",  # 86 HALF MOON LANE, LONDON
            "10090283768",  # KILIMANJARO LIVE LTD, SECOND FLOOR NORTH 15 BERMONDSEY SQUARE, LONDON
            "200003492155",  # BELLENDEN PRIMARY SCHOOL BELLENDEN ROAD, LONDON
            "10093341594",  # FLAT 6 4 JAMAICA ROAD, LONDON
            "10093341595",  # FLAT 7 4 JAMAICA ROAD, LONDON
            "10093339544",  # LONDON HOUSING FOUNDATION LTD, GROUND FLOOR REAR TEMPUS WHARF 29 BERMONDSEY WALL WEST, LONDON
            "200003468937",  # GROUNDSMANS COTTAGE COLLEGE ROAD, LONDON
            "10094086939",  # FLAT 4B 98 EAST DULWICH ROAD, LONDON
            "10091665680",  # 23 CAMBERWELL GROVE, LONDON
            "200003465665",  # 120 WARNER ROAD, LONDON
            "10093340214",  # SPORTS DIRECT, 91 RYE LANE, LONDON
            "10091665874",  # FLAT A 156 LOWER ROAD, LONDON
        ]:
            return None

        if record.addressline6 in [
            "SE5 0SY",
            "SE15 5AD",
            "SE1 2PS",
            "SE5 7HY",
            "SE15 6BJ",
            "SE1 3UL",
            "SE16 2QU",
            "SE16 6AZ",
            "SE1 2AD",
            "SE15 2FF",
            "SE1 0AA",
            "SE1 0NS",
            "SE15 3DN",
            "SE5 0HB",
            "SE15 2ND",
        ]:
            return None

        if record.addressline1 == "Excluding Third Floor and Fourth Floor":
            return None

        return super().address_record_to_dict(record)
