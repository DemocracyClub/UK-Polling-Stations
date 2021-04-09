from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TOR"
    addresses_name = (
        "2021-03-23T12:10:44.162180/Torridge Democracy_Club__06May2021 (1).tsv"
    )
    stations_name = (
        "2021-03-23T12:10:44.162180/Torridge Democracy_Club__06May2021 (1).tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Buckland Filleigh Parish Hall BUCKLAND FILLEIGH
        if record.polling_place_id == "8008":
            record = record._replace(polling_place_postcode="EX21 5HZ")

        # St Giles In the Wood Parish Hall St Giles In the Wood TORRINGTON
        if record.polling_place_id == "8005":
            record = record._replace(polling_place_postcode="EX38 7JH")

        # Bradworthy Methodist Chapel - School Room North Road Bradworthy EX22 7TS
        if record.polling_place_id == "7889":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002297638",  # GREAT DARRACOTT, TORRINGTON
            "10090288565",  # 19 BUCKLAND VIEW, BIDEFORD
            "10023353087",  # FOXLEIGH, ABBOTSHAM, BIDEFORD
            "10023352955",  # CASTLEBARNS, ABBOTSHAM, BIDEFORD
            "10002301906",  # FOLLYFOOT MANOR, SANDYMERE ROAD, NORTHAM, BIDEFORD
            "100040373290",  # MARSHFORD NURSERIES, CHURCHILL WAY, NORTHAM, BIDEFORD
            "100040374234",  # EARLSWOOD, DIDDYWELL ROAD, NORTHAM, BIDEFORD
            "100040374229",  # KOVERSADA, DIDDYWELL ROAD, APPLEDORE, BIDEFORD
            "100040370454",  # 2 GREEN LANE, APPLEDORE, BIDEFORD
            "10023353009",  # LUNDY VIEW, ABBOTSHAM, BIDEFORD
            "10003506157",  # CLIFFORD MILL, HIGHER CLOVELLY, BIDEFORD
            "10002302579",  # KNAPP SHIPPEN, HARTLAND, BIDEFORD
            "10003506169",  # WATERGAP, HARTLAND, BIDEFORD
            "200001644184",  # SPRUCE COTTAGE, HARTLAND, BIDEFORD
            "10002300015",  # THISTLEDOWN, BUCKLAND BREWER, BIDEFORD
            "10003506186",  # HONEYSUCKLE COTTAGE ROAD PAST WEST ASH FARM, FRITHELSTOCK
            "10002300509",  # 1 YEO FARM COTTAGES, YEO VALE, BIDEFORD
            "10003507564",  # LITTLE LAMBERT, PETERS MARLAND, TORRINGTON
            "10091080003",  # STORMWATCH MOBILE HOME, HOLSWORTHY
            "10093913426",  # OLD STABLES CARAVAN, MIDDLECOTT, BRANDIS CORNER, HOLSWORTHY
            "10002298999",  # BUCKHORN HOUSE, CLAWTON, HOLSWORTHY
            "10003503734",  # CAREY VIEW, ASHMILL, ASHWATER, BEAWORTHY
            "10093911854",  # MOON HOUSE, ASHMILL, ASHWATER, BEAWORTHY
            "10093911853",  # BRIDGE HOUSE, ASHMILL, ASHWATER, BEAWORTHY
        ]:
            return None

        if record.addressline6 in [
            "EX39 3TP",
            "EX39 3NZ",
            "EX39 1HA",
            "EX39 1HB",
            "EX39 5ED",
            "EX39 5PN",
            "EX39 1PU",
            "EX22 6QF",
            "EX21 5HN",
            "EX22 7TD",
            "EX39 5HQ",
            "EX22 7XE",
            "EX39 2BH",
            "EX22 7DQ",
            "EX39 3BU",
            "EX39 3DR",
            "EX39 1LF",
            "EX39 5JL",
            "EX39 3LX",
        ]:
            return None

        return super().address_record_to_dict(record)
