from data_importers.management.commands import BaseHalaroseCsvImporter


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
