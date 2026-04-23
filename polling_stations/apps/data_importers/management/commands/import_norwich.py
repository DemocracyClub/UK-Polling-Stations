from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = "2026-05-07/2026-04-08T13:23:22.994652/NOW_districts_UTF8.csv"
    stations_name = (
        "2026-05-07/2026-04-08T13:23:22.994652/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # The folowing are station coord corrections supplied by council:
        # PILLING PARK COMMUNITY CENTRE, 23 PILLING PARK ROAD, NORWICH, NR1 4PA
        if record.stationcode == "10CR1":
            record = record._replace(
                xordinate="625232",
                yordinate="308966",
            )
        # JENNY LIND COMMUNITY ROOM, VAUXHALL STREET ENTRANCE, 24 SUFFOLK SQUARE, NORWICH, NR2 2AA
        if record.stationcode == "45TO1":
            record = record._replace(
                xordinate="622281",
                yordinate="308083",
            )
        # HOLY TRINITY CHURCH HALL (FORMERLY CAMBRIDGE STREET HALL), 54 CAMBRIDGE STREET , NORWICH, NR2 2BB
        if record.stationcode == "46TO2":
            record = record._replace(
                xordinate="622143",
                yordinate="307970",
            )
        # DOURO PLACE CHAPEL, DOURO PLACE, DEREHAM ROAD, NORWICH, NR2 4BQ
        if record.stationcode == "36NE5":
            record = record._replace(
                xordinate="622036",
                yordinate="308860",
            )
        # WEST EARLHAM COMMUNITY CENTRE, 10 WILBERFORCE ROAD, NORWICH, NR5 8ND
        if record.stationcode == "5UN5A":
            record = record._replace(
                xordinate="619054",
                yordinate="308709",
            )
        # ST MARY'S CHURCH HALL, HUTCHINSON ROAD, NORWICH, NR5 8LB
        if record.stationcode == "50UN1":
            record = record._replace(
                xordinate="619518",
                yordinate="308821",
            )
        # ALIVE HOUSE, NELSON STREET, NORWICH NR2 4DR
        if record.stationcode == "55WE2":
            record = record._replace(
                xordinate="621730",
                yordinate="309508",
            )
        # ST MATTHEW'S CHURCH, TELEGRAPH LANE WEST, NORWICH, NR1 4JA
        if record.stationcode == "44TH4":
            record = record._replace(
                xordinate="624347",
                yordinate="308888",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # looks wrong
            "NR5 8NA",
        ]:
            return None

        return super().address_record_to_dict(record)
