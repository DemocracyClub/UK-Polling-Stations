from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "BIR"
    addresses_name = "2024-05-02/2024-03-18T17:12:50.103093/Eros_SQL_Output070.csv"
    stations_name = "2024-05-02/2024-03-18T17:12:50.103093/Eros_SQL_Output070.csv"
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # postcode correction for: St Mary and Ambrose Church Hall, Pershore Road, B5 7RL
        if record.pollingstationnumber in ["123", "124"]:
            record = record._replace(pollingstationpostcode="B5 7RA")

        # postcode correction for: The Good Shepherd Hall, R/O St Andrews Church, Slack Lane, B20 9RE
        if record.pollingstationnumber in ["180", "181"]:
            record = record._replace(pollingstationpostcode="B21 9RE")

        # Removing wrong UPRNs:

        # Birchfield Primary School, Trinity Road B6 6AJ
        # suggested UPRN: 100071470999
        if self.get_station_hash(record) == "30-birchfield-primary-school":
            record = record._replace(pollingvenueuprn="")

        # George Dixon Primary School, City Road B17 8LE
        # suggested UPRN: 100071411446
        if self.get_station_hash(record) in (
            "276-george-dixon-primary-school",
            "277-george-dixon-primary-school",
        ):
            record = record._replace(pollingvenueuprn="")

        # St Mary's Catholic Primary School, Vivian Road B17 0DN
        # suggested UPRN: 100071417689
        if self.get_station_hash(record) in (
            "173-st-marys-catholic-primary-school",
            "172-st-marys-catholic-primary-school",
        ):
            record = record._replace(pollingvenueuprn="")

        # Grove Hall, Grove Lane B17 0QB
        # suggested UPRN: can't find in addressbase, postcode might be wrong?
        if self.get_station_hash(record) in (
            "174-grove-hall",
            "175-grove-hall",
        ):
            record = record._replace(pollingvenueuprn="")

        # Wattville Primary School, Wattville Road B21 0DP
        # suggested UPRN: 100071440040
        if self.get_station_hash(record) in (
            "211-wattville-primary-school",
            "210-wattville-primary-school",
        ):
            record = record._replace(pollingvenueuprn="")

        # Shenley Lane Community Association & Sports Centre, 472 Shenley Lane B29 4HZ
        # suggested UPRN: 100070510240
        if (
            self.get_station_hash(record)
            == "15-shenley-lane-community-association-sports-centre"
        ):
            record = record._replace(pollingvenueuprn="")

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
        ]:
            return None

        if record.housepostcode in [
            # splits
            "B31 2AE",
            "B75 5QB",
            "B34 6NE",
            "B23 5AL",
            "B34 6HN",
            "B75 5NE",
            "B31 5NH",
            "B26 3HH",
            "B31 3JE",
            "B10 9JS",
            "B20 3QT",
            "B32 2NT",
            "B31 1AE",
            "B13 9UA",
            "B31 2FL",
            "B28 9QL",
            "B24 9HX",
            "B23 7XE",
            "B18 5BU",
            "B33 9QD",
            # looks wrong
            "B32 3QY",
            "B33 0AW",
            "B20 2RW",
        ]:
            return None

        return super().address_record_to_dict(record)

    # quick fix to show maps for Halarose records that have a valid UPRN in the PollingVenueUPRN field
    def get_station_point(self, record):
        uprn = record.pollingvenueuprn.strip().lstrip("0")
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except ObjectDoesNotExist:
            return super().get_station_point(record)
