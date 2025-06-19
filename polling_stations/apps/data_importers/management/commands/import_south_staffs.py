from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SST"
    addresses_name = (
        "2025-06-26/2025-06-19T20:52:32.985120/Democracy_Club__26June2025.tsv"
    )
    stations_name = (
        "2025-06-26/2025-06-19T20:52:32.985120/Democracy_Club__26June2025.tsv"
    )
    elections = ["2025-06-26"]
    csv_delimiter = "\t"
    # by-election so maintaining previous exclusions for easy reference
    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")

    #     if (
    #         uprn
    #         in [
    #             "100031833008",  # CHILLINGTON LODGE, WHITEHOUSE LANE, CODSALL WOOD, WOLVERHAMPTON
    #             "100031799992",  # GREENSFORGE HOUSE, GREENSFORGE, KINGSWINFORD, DY6 0AH
    #             "200004524554",  # IVETSEY BANK FARM, IVETSEY BANK, WHEATON ASTON, STAFFORD
    #             "10094875300",  # POOL FARM BUNGALOW, GAILEY LEA LANE, GAILEY, STAFFORD ST19 5PT
    #             "100032282008",  # SHOOT LODGE, TEDDESLEY ROAD, PENKRIDGE, STAFFORD
    #             "10090093164",  # 3 HAY HOUSE COURT, DUNSTON HEATH, STAFFORD
    #             "10090091050",  # 2 HAY HOUSE COURT, DUNSTON HEATH, STAFFORD
    #             "10090091049",  # 1 HAY HOUSE COURT, DUNSTON HEATH, STAFFORD
    #             "200004526134",  # 135 RODBASTON, PENKRIDGE, STAFFORD
    #             "200004528062",  # AMBLESIDE, WOLVERHAMPTON ROAD, PENKRIDGE, STAFFORD
    #             "10003692787",  # 7B SANDYFIELDS ROAD, DUDLEY
    #             "10003693861",  # WILD WOOD, COUNTY LANE, ALBRIGHTON, WOLVERHAMPTON
    #             "10003693386",  # M S J HEALTHCARE, KARTER FARM, NEW ROAD, SWINDON, DUDLEY
    #         ]
    #     ):
    #         return None

    #     if record.addressline6 in [
    #         # splits
    #         "ST19 9AG",
    #         "WV9 5BW",
    #         "WV11 2DN",
    #         "ST19 9AB",
    #         # suspect
    #         "WV5 8EX",
    #         "WV11 2RD",
    #         "ST19 9LX",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)

    # def station_record_to_dict(self, record):
    #     # Ignore warning: Polling station Hyde Lea Village Hall (6031) is in Stafford Borough Council (STA)
    #     # Location is correct, just outside of the council border

    #     # Point correction for: St Bartholomew's Church Hall, Vicarage Road, Penn, Wolverhampton, WV4 5HU
    #     # Ignore warning: Polling station St Bartholomew's Church Hall (6225) is in Wolverhampton City Council
    #     if record.polling_place_id == "6225":
    #         record = record._replace(
    #             polling_place_easting="389364", polling_place_northing="295314"
    #         )

    #     # coords and UPRN from council for the following stations:
    #     # The Shepherds Buildings, Burnhill Green, WV6 7JA
    #     if record.polling_place_id == "6244":
    #         record = record._replace(
    #             polling_place_easting="378976",
    #             polling_place_northing="300293",
    #             polling_place_uprn="200004521936",
    #         )
    #     # Wombourne Village Hall, High Street, Wombourne, Wolverhampton, WV5 9DT
    #     if record.polling_place_id == "6221":
    #         record = record._replace(
    #             polling_place_easting="387823",
    #             polling_place_northing="293176",
    #             polling_place_uprn="200004528646",
    #         )

    #     return super().station_record_to_dict(record)
