from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PRE"
    addresses_name = (
        "2023-05-04/2023-04-17T11:55:49.360892/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-17T11:55:49.360892/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007606520",  # WILLOW BANK, INGLEWHITE ROAD, GOOSNARGH, PRESTON
            "100010579401",  # 16A WOODPLUMPTON ROAD, ASHTON-ON-RIBBLE, PRESTON
            "100010574023",  # 219 TULKETH BROW, ASHTON-ON-RIBBLE, PRESTON
            "100012402901",  # MEADOWBROOK, INGLEWHITE ROAD, GOOSNARGH, PRESTON
            "10093763454",  # 2 SHEARDLEY AVENUE, PRESTON
            "10007602677",  # 1 COW HILL, HAIGHTON, PRESTON
            "10007601000",  # NORTH LODGE, MOOR PARK, PRESTON
            "100012402882",  #  1 OAK TREE FARM INGLEWHITE ROAD, PRESTON
            "10007606525",  # 2 OAK TREE FARM INGLEWHITE ROAD, PRESTON
        ]:
            return None

        if record.addressline6 in [
            # Odd looking, overlapping with other stations
            "PR4 0FG",  # ALDEBURGH DRIVE, LIGHTFOOT GREEN, PRESTON
            "PR4 0EX",  # REDWOOD DRIVE, COTTAM, PRESTON
            "PR4 0PW",  # BUCKTHORN DRIVE, COTTAM, PRESTON
            "PR1 3SG",  # FOUNDATIONS OXFORD STREET, PRESTON
            "PR2 5PZ",  # NORMAN JEPSON TRAVEL INN BLUEBELL WAY, PRESTON
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Millennium Hall, Neapsands Close, Fulwood, Preston, PR2 9AQ
        if record.polling_place_id == "4401":
            record = record._replace(
                polling_place_easting="355834", polling_place_northing="432408"
            )

        # Goosnargh Village Hall, Church Lane, Goosnargh, Preston, PR3 2BH
        if record.polling_place_id == "4459":
            record = record._replace(
                polling_place_easting="355843", polling_place_northing="436739"
            )
        return super().station_record_to_dict(record)
