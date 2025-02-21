from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAT"
    addresses_name = (
        "2025-03-06/2025-02-21T11:01:39.239611/Democracy_Club__06March2025.CSV"
    )
    stations_name = (
        "2025-03-06/2025-02-21T11:01:39.239611/Democracy_Club__06March2025.CSV"
    )
    elections = ["2025-03-06"]

    # preserving 2024 GE exclusions for future reference
    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")

    #     if (
    #         uprn
    #         in [
    #             "100060835439",  # 22 MICKLEBURGH HILL, HERNE BAY
    #             "10094583530",  # SHIRE COTTAGE, FORD, HOATH, CANTERBURY
    #             "200000690267",  # DO BURRIDGE & SON, THRUXTED FARM, PENNY POT LANE, MYSTOLE, CANTERBURY
    #             "10090316068",  # 11B BEACONSFIELD ROAD, CANTERBURY
    #             "100060808344",  # 11A BEACONSFIELD ROAD, CANTERBURY
    #             "100060808340",  # 7 BEACONSFIELD ROAD, CANTERBURY
    #             "100060808342",  # 9 BEACONSFIELD ROAD, CANTERBURY
    #             "100060808345",  # 11 BEACONSFIELD ROAD, CANTERBURY
    #             "100060808347",  # 13 BEACONSFIELD ROAD, CANTERBURY
    #             "100060808349",  # 15 BEACONSFIELD ROAD, CANTERBURY
    #             "100060808351",  # 17 BEACONSFIELD ROAD, CANTERBURY
    #             "100060816786",  # HOLMLEA, MANDEVILLE ROAD, CANTERBURY
    #             "200000675476",  # WHITEHALL FARM, WHITEHALL ROAD, CANTERBURY
    #             "100062280306",  # 57 NUNNERY FIELDS, CANTERBURY
    #             "200000696793",  # HOWLETTS WILD ANIMAL PARK, BEKESBOURNE ROAD, BEKESBOURNE, CANTERBURY
    #             "100060829891",  # 69A BROOMFIELD ROAD, HERNE BAY
    #             "100060829893",  # 71 BROOMFIELD ROAD, HERNE BAY
    #             "10033155183",  # THE BUNGALOW, PALMSTEAD, UPPER HARDRES, CANTERBURY
    #         ]
    #     ):
    #         return None

    #     if record.addressline6 in [
    #         # splits
    #         "CT1 3ZE"
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)
