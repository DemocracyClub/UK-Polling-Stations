from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "BIR"
    addresses_name = "2026-05-07/2026-03-16T17:42:35.689839/Democracy Club - Idox_2026-03-16 17-34.csv"
    stations_name = "2026-05-07/2026-03-16T17:42:35.689839/Democracy Club - Idox_2026-03-16 17-34.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # postcode correction for: St Mary and Ambrose Church Hall, Pershore Road, B5 7RL
        if record.pollingstationnumber in ["123", "124"]:
            record = record._replace(pollingstationpostcode="B5 7RA")

        # postcode correction for: The Good Shepherd Hall, R/O St Andrews Church, Slack Lane, B20 9RE
        if record.pollingstationnumber in ["180", "181"]:
            record = record._replace(pollingstationpostcode="B21 9RE")

        # Removing wrong UPRNs and coordinates:
        if (
            self.get_station_hash(record)
            in [
                "30-birchfield-primary-school",  # Birchfield Primary School, Trinity Road B6 6AJ - suggested UPRN: 100071470999
                "174-grove-hall",  # Grove Hall, Grove Lane B17 0QB - suggested UPRN: can't find in addressbase, postcode might be wrong?
                "175-grove-hall",  # Grove Hall, Grove Lane B17 0QB - suggested UPRN: can't find in addressbase, postcode might be wrong?
                "15-shenley-lane-community-association-sports-centre",  # Shenley Lane Community Association & Sports Centre, 472 Shenley Lane B29 4HZ - suggested UPRN: 100070510240
                "172-st-marys-catholic-primary-school",  # St Mary's Catholic Primary School Vivian Road
                "173-st-marys-catholic-primary-school",  # St Mary's Catholic Primary School Vivian Road
            ]
        ):
            record = record._replace(
                pollingvenueuprn="", pollingvenueeasting=0, pollingvenuenorthing=0
            )

        # Corrected point for stations at:
        # Hut: Car Park Beggars Bush Public House Corner of Chester Road and Jockey Road
        if self.get_station_hash(record) in [
            "433-hut-car-park-beggars-bush-public-house",
            "432-hut-car-park-beggars-bush-public-house",
        ]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(409733, 294494, srid=27700)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10024448607",  # 71 PAGET ROAD, BIRMINGHAM
                "100070549934",  # 10 LENCHS CLOSE, BIRMINGHAM
                "100070549936",  # 12 LENCHS CLOSE, BIRMINGHAM
                "100070549938",  # 14 LENCHS CLOSE, BIRMINGHAM
                "100070549940",  # 16 LENCHS CLOSE, BIRMINGHAM
                "100070549942",  # 18 LENCHS CLOSE, BIRMINGHAM
                "100071313853",  # THE BUNGALOW, WALMLEY ASH LANE, MINWORTH, SUTTON COLDFIELD
                "100070510807",  # 4 SHERBOURNE ROAD, ACOCKS GREEN, BIRMINGHAM
                "100070558277",  # 163 WEST HEATH ROAD, NORTHFIELD, BIRMINGHAM
                "10023506546",  # 31 REA ROAD, NORTHFIELD, BIRMINGHAM
                "10023506547",  # 27 REA ROAD, NORTHFIELD, BIRMINGHAM
                "10023506544",  # 33 REA ROAD, NORTHFIELD, BIRMINGHAM
                "10023506545",  # 29 REA ROAD, NORTHFIELD, BIRMINGHAM
                "100070526161",  # 145 STONEHOUSE LANE, QUINTON, BIRMINGHAM
                "100070526157",  # 141 STONEHOUSE LANE, QUINTON, BIRMINGHAM
                "100070526159",  # 143 STONEHOUSE LANE, QUINTON, BIRMINGHAM
                "100071312729",  # FLAT THE FOX AND DOGS LITTLE SUTTON ROAD, SUTTON COLDFIELD, B75 6QB
                "100071267937",  # FLAT OVER CAMP 1 CAMP LANE, KINGS NORTON, BIRMINGHAM, B38 8SP
                "100070535261",  # 230 THE BROADWAY, BIRMINGHAM, B20 3DL
            ]
        ):
            return None

        if record.postcode in [
            # splits
            "B34 6HN",
            "B13 9UA",
            "B10 9JS",
            "B75 5NE",
            "B34 6NE",
            "B20 3QT",
            "B28 9QL",
            "B26 3HH",
            "B32 2NT",
            "B31 3JE",
            "B32 2JL",
            "B33 9QD",
            "B31 2FL",
            "B23 5AL",
            "B31 5NH",
            "B75 5QB",
            "B31 2AE",
            "B72 1JY",
            "B11 1LJ",
            # looks wrong
            "B32 3QY",
            "B33 0AW",
            "B20 2RW",
            "B75 7LJ",
            "B5 7SS",
        ]:
            return None
        return super().address_record_to_dict(record)
