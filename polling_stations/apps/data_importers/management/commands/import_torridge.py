from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TOR"
    addresses_name = (
        "2025-05-01/2025-03-24T16:40:14.513884/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-24T16:40:14.513884/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-04-17", "2025-05-01"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # postcode correction for: West Croft School, Coronation Road, Bideford, EX39 3DD
        if record.polling_place_id == "9368":
            record = record._replace(polling_place_postcode="EX39 3DE")

        # point correction for: Torrington Methodist Church Hall - The Hall, Windy Cross, TORRINGTON, EX38 8AL
        # point correction for: Torrington Methodist Church Hall - Creche, Windy Cross, TORRINGTON, EX38 8AL
        if record.polling_place_id in ["9533", "9529"]:
            record = record._replace(
                polling_place_easting="249335", polling_place_northing="119076"
            )

        # add postcode for: Newton St Petrock Community Centre, Newton St Petrock
        if record.polling_place_id == "9435":
            record = record._replace(polling_place_postcode="EX22 7LW")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002297638",  # GREAT DARRACOTT, TORRINGTON
            "10023353087",  # FOXLEIGH, ABBOTSHAM, BIDEFORD
            "10002301906",  # FOLLYFOOT MANOR, SANDYMERE ROAD, NORTHAM, BIDEFORD
            "100040374234",  # EARLSWOOD, DIDDYWELL ROAD, NORTHAM, BIDEFORD
            "100040374229",  # KOVERSADA, DIDDYWELL ROAD, APPLEDORE, BIDEFORD
            "100040370454",  # 2 GREEN LANE, APPLEDORE, BIDEFORD
            "10023353009",  # LUNDY VIEW, ABBOTSHAM, BIDEFORD
            "10003506157",  # CLIFFORD MILL, HIGHER CLOVELLY, BIDEFORD
            "10002302579",  # KNAPP SHIPPEN, HARTLAND, BIDEFORD
            "10003506169",  # WATERGAP, HARTLAND, BIDEFORD
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
            "10002299506",  # FLAT LITTLE BURSDON ROAD PAST EAST BURSDON FARM, HARTLAND
            "10090289801",  # LITTLE BURSDON CARAVAN, HARTLAND, BIDEFORD
            "10002300463",  # LITTLE BURSDON, HARTLAND, BIDEFORD
            "10003506595",  # TREVENNA, HARTLAND, BIDEFORD
            "200001768435",  # SMUGGLERS COTTAGE, BUCKS MILLS, BIDEFORD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "EX39 1PU",
            "EX38 8NN",
            "EX38 7JY",
            "EX22 7BU",
            "EX21 5HN",
            "EX22 7XE",
            "EX39 3LX",
            # suspect
            "EX39 3TP",
            "EX39 1HA",
            "EX39 1HB",
            "EX39 5ED",
            "EX38 8BJ",
            "EX22 7NA",
            "EX39 1LE",
        ]:
            return None

        return super().address_record_to_dict(record)
