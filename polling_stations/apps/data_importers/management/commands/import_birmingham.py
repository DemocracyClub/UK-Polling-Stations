from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "BIR"
    addresses_name = "2024-07-04/2024-06-27T08:30:10.119012/Eros_SQL_Output077.csv"
    stations_name = "2024-07-04/2024-06-27T08:30:10.119012/Eros_SQL_Output077.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # postcode correction for: St Mary and Ambrose Church Hall, Pershore Road, B5 7RL
        if record.pollingstationnumber in ["18", "19"]:
            record = record._replace(pollingstationpostcode="B5 7RA")

        # postcode correction for: The Good Shepherd Hall, R/O St Andrews Church, Slack Lane, B20 9RE
        if record.pollingstationnumber in ["314", "315"]:
            record = record._replace(pollingstationpostcode="B21 9RE")

        # Removing wrong UPRNs:
        if self.get_station_hash(record) in [
            "297-birchfield-primary-school",  # Birchfield Primary School, Trinity Road B6 6AJ - suggested UPRN: 100071470999
            "36-barford-primary-school-nursery-unit",  # George Dixon Primary School, City Road B17 8LE - suggested UPRN: 100071411446
            "38-george-dixon-primary-school",  # George Dixon Primary School, City Road B17 8LE - suggested UPRN: 100071411446
            "37-george-dixon-primary-school",  # George Dixon Primary School, City Road B17 8LE - suggested UPRN: 100071411446
            "9-st-marys-catholic-church-hall",  # St Mary's Catholic Primary School, Vivian Road B17 0DN - suggested UPRN: 100071417689
            "10-st-marys-catholic-church-hall",  # St Mary's Catholic Primary School, Vivian Road B17 0DN - suggested UPRN: 100071417689
            "31-grove-hall",  # Grove Hall, Grove Lane B17 0QB - suggested UPRN: can't find in addressbase, postcode might be wrong?
            "32-grove-hall",  # Grove Hall, Grove Lane B17 0QB - suggested UPRN: can't find in addressbase, postcode might be wrong?
            "321-wattville-primary-school",  # Wattville Primary School, Wattville Road B21 0DP - suggested UPRN: 100071440040
            "320-wattville-primary-school",  # Wattville Primary School, Wattville Road B21 0DP - suggested UPRN: 100071440040
            "245-shenley-lane-community-association-sports-centre",  # Shenley Lane Community Association & Sports Centre, 472 Shenley Lane B29 4HZ - suggested UPRN: 100070510240
            "322-wattville-primary-school",  # Wattville Primary School Wattville Road
            "29-st-marys-catholic-primary-school",  # St Mary's Catholic Primary School Vivian Road
            "30-st-marys-catholic-primary-school",  # St Mary's Catholic Primary School Vivian Road
        ]:
            record = record._replace(pollingvenueuprn="")

        # Corrected point for stations at:
        # Hut: Car Park Beggars Bush Public House Corner of Chester Road and Jockey Road
        if self.get_station_hash(record) in [
            "462-hut-car-park-beggars-bush-public-house",
            "463-hut-car-park-beggars-bush-public-house",
        ]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(409733, 294494, srid=27700)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10024448607",  # 71 PAGET ROAD, BIRMINGHAM
            "10023295371",  # 10A GROSVENOR ROAD, QUINTON, BIRMINGHAM
            "100070549934",  # 10 LENCHS CLOSE, BIRMINGHAM
            "10023509817",  # 1 MOAT DRIVE, BUCKLAND END, BIRMINGHAM
            "100070549936",  # 12 LENCHS CLOSE, BIRMINGHAM
            "100070549938",  # 14 LENCHS CLOSE, BIRMINGHAM
            "100070549940",  # 16 LENCHS CLOSE, BIRMINGHAM
            "100070549942",  # 18 LENCHS CLOSE, BIRMINGHAM
            "100070607561",  # 2B WHITE FARM ROAD, SUTTON COLDFIELD
            "100070607560",  # 2A WHITE FARM ROAD, SUTTON COLDFIELD
            "100071313853",  # THE BUNGALOW, WALMLEY ASH LANE, MINWORTH, SUTTON COLDFIELD
            "100070510807",  # 4 SHERBOURNE ROAD, ACOCKS GREEN, BIRMINGHAM
            "100070558277",  # 163 WEST HEATH ROAD, NORTHFIELD, BIRMINGHAM
            "100070414537",  # 5 ICKNIELD PORT ROAD, BIRMINGHAM
            "100070414534",  # 2 ICKNIELD PORT ROAD, BIRMINGHAM
            "100070414533",  # 1 ICKNIELD PORT ROAD, BIRMINGHAM
            "100070414535",  # 3 ICKNIELD PORT ROAD, BIRMINGHAM
            "100070414536",  # 4 ICKNIELD PORT ROAD, BIRMINGHAM
            "10023506546",  # 31 REA ROAD, NORTHFIELD, BIRMINGHAM
            "10023506547",  # 27 REA ROAD, NORTHFIELD, BIRMINGHAM
            "10023506544",  # 33 REA ROAD, NORTHFIELD, BIRMINGHAM
            "10023506545",  # 29 REA ROAD, NORTHFIELD, BIRMINGHAM
            "100070526161",  # 145 STONEHOUSE LANE, QUINTON, BIRMINGHAM
            "100070526157",  # 141 STONEHOUSE LANE, QUINTON, BIRMINGHAM
            "100070526159",  # 143 STONEHOUSE LANE, QUINTON, BIRMINGHAM
        ]:
            return None

        if record.housepostcode in [
            # splits
            "B32 2NT",
            "B31 5NH",
            "B23 5AL",
            "B26 3HH",
            "B31 2FL",
            "B10 9JS",
            "B20 3QT",
            "B13 9UA",
            "B75 5NE",
            "B31 1AE",
            "B75 5QB",
            "B34 6HN",
            "B34 6NE",
            "B23 7XE",
            "B11 1LJ",
            "B31 2AE",
            "B28 9QL",
            "B18 5BU",
            "B31 3JE",
            "B33 9QD",
            "B24 9HX",
            # looks wrong
            "B32 3QY",
            "B33 0AW",
            "B20 2RW",
        ]:
            return None
        return super().address_record_to_dict(record)
