from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = "2026-05-07/2026-04-08T13:23:22.994652/NOW_districts_UTF8.csv"
    stations_name = (
        "2026-05-07/2026-04-08T13:23:22.994652/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # removing bad coordinates pending council response:
        if (
            record.stationcode
            in [
                "10CR1",  # PILLING PARK COMMUNITY CENTRE, 23 PILLING PARK ROAD, NORWICH, NR1 4PA
                "45TO1",  # JENNY LIND COMMUNITY ROOM, VAUXHALL STREET ENTRANCE, 24 SUFFOLK SQUARE, NORWICH, NR2 2AA
                "46TO2",  # HOLY TRINITY CHURCH HALL (FORMERLY CAMBRIDGE STREET HALL), 54 CAMBRIDGE STREET , NORWICH, NR2 2BB
                "36NE5",  # DOURO PLACE CHAPEL, DOURO PLACE, DEREHAM ROAD, NORWICH, NR2 4BQ
                "5UN5A",  # WEST EARLHAM COMMUNITY CENTRE, 10 WILBERFORCE ROAD, NORWICH, NR5 8ND
                "50UN1",  # ST MARY'S CHURCH HALL, HUTCHINSON ROAD, NORWICH, NR5 8LB
                "55WE2",  # ALIVE HOUSE, NELSON STREET, NORWICH NR2 4DR
                "44TH4",  # ST MATTHEW'S CHURCH, TELEGRAPH LANE WEST, NORWICH, NR1 4JA
            ]
        ):
            record = record._replace(xordinate="0", yordinate="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # looks wrong
            "NR5 8NA",
        ]:
            return None

        return super().address_record_to_dict(record)
