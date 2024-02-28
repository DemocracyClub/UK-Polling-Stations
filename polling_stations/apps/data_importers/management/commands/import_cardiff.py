from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRF"
    addresses_name = (
        "2024-05-02/2024-02-28T12:41:47.011342/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-28T12:41:47.011342/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Community Suite, Llanishen Leisure Centre, Ty Glas Avenue, Llanishen, Cardiff
        if record.polling_place_id == "20459":
            # geocode was a way off, postcode was right, but found the building so here it is anyway
            record = record._replace(polling_place_uprn="10002526454")

        # Canolfan Beulah, (Church Community Centre), Beulah Crossroads, Rhiwbina, Cardiff, CF14 6AX
        if record.polling_place_id == "20483":
            record = record._replace(polling_place_postcode="CF14 6LT")

        # The Church Hall, Kelston Road, Whitchurch, Cardiff
        if record.polling_place_id == "20496":
            record = record._replace(polling_place_uprn="200001850852")

        # St Mary`s Church Hall, Church Road, Cardiff, CF14 2ED
        # Council request to use below postcode, ignore the warning
        if record.polling_place_id == "20499":
            record = record._replace(
                polling_place_postcode="CF14 2DX", polling_place_uprn="10008903814"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100100127979",  # 17 LON-Y-RHYD, CARDIFF
            "100100110392",  # 10 SOMERSET COURT, BURNHAM AVENUE, LLANRUMNEY, CARDIFF
            "100100107993",  # 890 NEWPORT ROAD, RUMNEY, CARDIFF
            "100100107313",  # 45 LLANSTEPHAN ROAD, RUMNEY, CARDIFF
            "10002524512",  # CLUB HOUSE RUMNEY R F C HARTLAND ROAD, LLANRUMNEY, CARDIFF
            "10008904957",  # OAK HOUSE, 340 NEWPORT ROAD, CARDIFF
            "100100066910",  # 1 WHITMUIR ROAD, CARDIFF
            "10090486882",  # SECOND FLOOR DOCK CHAMBERS 5 BUTE STREET, BUTETOWN, CARDIFF
            "200002932357",  # 46 AMHERST STREET, CARDIFF
            "200002932358",  # 48 AMHERST STREET, CARDIFF
            "200002932356",  # 44 AMHERST STREET, CARDIFF
            "10090488749",  # 456A COWBRIDGE ROAD EAST, CARDIFF
            "10092985344",  # FIRST FLOOR FLAT 452 COWBRIDGE ROAD EAST, CANTON, CARDIFF
            "100101043751",  # VVV RETAIL LTD, THE CABIN, WAUNGRON ROAD, CARDIFF
            "100100094616",  # CROSSLANDS CHILDRENS UNIT, 318 COWBRIDGE ROAD WEST, CARDIFF
            "100100098970",  # 144 SNOWDEN ROAD, CARDIFF
            "100100094085",  # 2 CAERWENT ROAD, CARDIFF
            "10002507423",  # MAES Y LLECH FARM, RADYR, CARDIFF
            "100100127342",  # 145 HEOL Y DERI, CARDIFF
            "100100896720",  # PARK HOUSE, MUIRTON ROAD, CARDIFF
            "100100890356",  # UNIVERSITY CATHOLIC CHAPLAINCY, 62 PARK PLACE, CARDIFF
            "100100094728",  # 7 CROSSWAYS ROAD, CARDIFF
            "100100139505",  # WHITE LODGE, CHURCH ROAD, PENTYRCH, CARDIFF
            "10002509001",  # LLANFAIR COURT, ST. Y NYLL LANE, CAPEL LLANILLTERN, CARDIFF
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CF15 8EL",
            "CF24 2DG",
            # looks wrong
            "CF3 1XY",
            "CF24 2EE",
            "CF24 0DF",
            "CF11 6BN",
            "CF5 5SB",
            "CF14 9UA",
        ]:
            return None

        return super().address_record_to_dict(record)
