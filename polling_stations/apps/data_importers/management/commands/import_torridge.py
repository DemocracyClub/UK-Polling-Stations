from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TOR"
    addresses_name = (
        "2024-05-02/2024-02-22T16:57:01.775461/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-22T16:57:01.775461/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # West Croft School, Coronation Road, Bideford, EX39 3DD
        if record.polling_place_id == "8565":
            record = record._replace(polling_place_postcode="EX39 3DE")

        # Torrington Methodist Church Hall - The Hall, Windy Cross, TORRINGTON, EX38 8AL
        # Torrington Methodist Church Hall - Creche, Windy Cross, TORRINGTON, EX38 8AL
        if record.polling_place_id in ["8619", "8623"]:
            record = record._replace(
                polling_place_easting="249335", polling_place_northing="119076"
            )

        # Newton St Petrock Community Centre, Newton St Petrock
        if record.polling_place_id == "8679":
            record = record._replace(polling_place_postcode="EX22 7LW")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002297638",  # GREAT DARRACOTT, TORRINGTON
            "10023353087",  # FOXLEIGH, ABBOTSHAM, BIDEFORD
            "10002301906",  # FOLLYFOOT MANOR, SANDYMERE ROAD, NORTHAM, BIDEFORD
            "100040373290",  # MARSHFORD NURSERIES, CHURCHILL WAY, NORTHAM, BIDEFORD
            "100040374234",  # EARLSWOOD, DIDDYWELL ROAD, NORTHAM, BIDEFORD
            "100040374229",  # KOVERSADA, DIDDYWELL ROAD, APPLEDORE, BIDEFORD
            "100040370454",  # 2 GREEN LANE, APPLEDORE, BIDEFORD
            "10023353009",  # LUNDY VIEW, ABBOTSHAM, BIDEFORD
            "10003506157",  # CLIFFORD MILL, HIGHER CLOVELLY, BIDEFORD
            "10002302579",  # KNAPP SHIPPEN, HARTLAND, BIDEFORD
            "10003506169",  # WATERGAP, HARTLAND, BIDEFORD
            "10002300015",  # THISTLEDOWN, BUCKLAND BREWER, BIDEFORD
            "10003506186",  # HONEYSUCKLE COTTAGE ROAD PAST WEST ASH FARM, FRITHELSTOCK
            "10002300509",  # 1 YEO FARM COTTAGES, YEO VALE, BIDEFORD
            "10093913426",  # OLD STABLES CARAVAN, MIDDLECOTT, BRANDIS CORNER, HOLSWORTHY
            "10002298999",  # BUCKHORN HOUSE, CLAWTON, HOLSWORTHY
            "10003503734",  # CAREY VIEW, ASHMILL, ASHWATER, BEAWORTHY
            "10093911854",  # MOON HOUSE, ASHMILL, ASHWATER, BEAWORTHY
            "10093911853",  # BRIDGE HOUSE, ASHMILL, ASHWATER, BEAWORTHY
            "10093910800",  # BYWATER HOUSE, SILFORD CROSS, WESTWARD HO, BIDEFORD
            "10003506177",  # THE COACH HOUSE, LITTLE SILVER, STEVENSTONE, TORRINGTON
            "10002301760",  # HIGHER COURT BARN, ST. GILES, TORRINGTON
            "10090288709",  # THE BEECHES, LIMERS LANE, NORTHAM, BIDEFORD
            "100040374230",  # THE COTTAGE, DIDDYWELL ROAD, NORTHAM, BIDEFORD
            "10003507823",  # STANLEIGH LODGE, DIDDYWELL ROAD, NORTHAM, BIDEFORD
            "10095917163",  # THE QUILLET CARAVAN, DIDDYWELL ROAD, APPLEDORE, BIDEFORD
            "10003506180",  # ORCHARD COTTAGE LANE TO WAY BARTON, ST GILES IN THE WOOD
            "10003506037",  # THE SPINNEY, WINSFORD LANE, HALWILL JUNCTION, BEAWORTHY
            "10091078138",  # WHEELERS RETREAT, BRADWORTHY, HOLSWORTHY
            "10002299506",  # FLAT LITTLE BURSDON ROAD PAST EAST BURSDON FARM, HARTLAND
            "10090289801",  # LITTLE BURSDON CARAVAN, HARTLAND, BIDEFORD
            "10002300463",  # LITTLE BURSDON, HARTLAND, BIDEFORD
            "10003506595",  # TREVENNA, HARTLAND, BIDEFORD
            "200001768435",  # SMUGGLERS COTTAGE, BUCKS MILLS, BIDEFORD
            "10002300522",  # HIGH PARK LODGE, LITTLEHAM, BIDEFORD
            "10090289146",  # APARTMENT 3436 WESTBEACH RESORT BATH HOTEL ROAD, WESTWARD HO!
            "10002299752",  # COMMON MOOR, CLAWTON, HOLSWORTHY
            "10093911404",  # MEADOW WOOD, FRITHELSTOCK, TORRINGTON
            "10003506170",  # BITEFORD, WOOLSERY, BIDEFORD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "EX38 8NN",
            "EX39 3LU",
            "EX39 5FL",
            "EX39 1PU",
            "EX39 3LX",
            "EX21 5HN",
            "EX22 7XE",
            # suspect
            "EX39 3TP",  # BUCKLAND VIEW, BIDEFORD
            "EX39 1HA",  # BURROWS WAY, NORTHAM, BIDEFORD
            "EX39 1HB",  # SANDYMERE ROAD, NORTHAM, BIDEFORD
            "EX39 5ED",  # WALLAND DRIVE, BUCKS CROSS, BIDEFORD
            "EX38 8BJ",  # KITCHENER ROW, CALF STREET, TORRINGTON
            "EX22 7NA",
            "EX22 7YH",
        ]:
            return None

        return super().address_record_to_dict(record)
