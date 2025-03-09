from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DUR"
    addresses_name = (
        "2025-05-01/2025-03-09T22:01:15.757058/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-09T22:01:15.757058/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10093427357",  # 100B SUNDERLAND ROAD, HORDEN
                "10013609644",  # 100 SUNDERLAND ROAD, HORDEN
                "100110527067",  # 1 FOUNDRY FIELDS, CROOK
                "200002973264",  # FURZEDOWN, LOW JOBS HILL, CROOK
                "100110741529",  # BONA CASA, WOODSIDE, SACRISTON, DURHAM
                "10002955293",  # WILLOW HOUSE, WOODSIDE, SACRISTON, DURHAM
                "200003837208",  # GREENBANK HOUSE, WOODSTONE VILLAGE, HOUGHTON LE SPRING
                "200003837203",  # WILLOW FARM STOVES, WILLOW FARM, WOODSTONE VILLAGE, HOUGHTON LE SPRING
                "100110741309",  # SUMMERHILL, PETH BANK, LANCHESTER, DURHAM
                "10014567760",  # FINES HOUSE QUEENS PARADE (SIDE), ANNFIELD PLAIN
                "10094019851",  # OLD FIELD HOUSE, ANNFIELD PLAIN, STANLEY
                "100110712083",  # FLAT WEST VIEW STOCKTON ROAD, SEAHAM
                "100110711512",  # ST, JOSEPHS PRESBYTERY, COAST ROAD, BLACKHALL COLLIERY, HARTLEPOOL
                "10012053828",  # THINFORD HOUSE THINFORD LANE, THINFORD
                "10012055410",  # CLEARWATER CREEK, DURHAM ROAD, COATHAM MUNDEVILLE, DARLINGTON
                "100110376637",  # 23A NELSON STREET, CONSETT
                "10013259154",  # FLAT AT PROSPECT BUILDINGS COAST ROAD, HORDEN
                "10014556760",  # LONGFIELD BARNARD CASTLE SCHOOL NEWGATE, BARNARD CASTLE
                "10093043991",  # 1 FRONT STREET FLEMING FIELD TRACK TO NORTH MOOR FARM, HASWELL
                "200003218251",  # 1 THE GATEHOUSE KEPIER FARM KEPIER LANE, GILESGATE
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "DL4 1DN",
            "DH8 8HN",
            "DH9 9JQ",
            "DH1 4NP",
            "DH2 2BL",
            "DL13 1ND",
            "DL12 9UR",
            "DL13 4NQ",
            "DL13 2AB",
            "SR7 9BS",
            "SR7 7NE",
            # looks wrong
            "DL5 5QS",
            "DH9 6SA",
            "DH2 2FL",
            "DH7 6NY",
            "DL5 5AH",
            "SR8 4QG",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Removing wrong coordinates for:
        # Great Lumley Methodist Church Hall, Front Street, Great Lumley, Chester le Street, Co Durham DH3 4JB
        if record.polling_place_id == "71962":
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )
        # The Cose, Bridge Creative, 1 Dorset Place, Henknowle, Bishop Auckland, Co Durham DL14 6TH
        if record.polling_place_id == "70811":
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )
        # Willington Library, 46a High Street, Willington, Crook DL15 0PG
        if record.polling_place_id == "71884":
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )
        return super().station_record_to_dict(record)
