from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2024-07-04/2024-06-20T16:15:36.856129/CAB_combined_v2.csv"
    stations_name = "2024-07-04/2024-06-20T16:15:36.856129/CAB_combined_v2.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090968298",  # FLAT 5, BURTON HOUSE 2A, ROCK ROAD, CAMBRIDGE
            "10090968296",  # FLAT 3, BURTON HOUSE 2A, ROCK ROAD, CAMBRIDGE
            "10090968295",  # FLAT 2, BURTON HOUSE 2A, ROCK ROAD, CAMBRIDGE
            "10090968294",  # FLAT 1, BURTON HOUSE 2A, ROCK ROAD, CAMBRIDGE
            "10090968297",  # FLAT 4, BURTON HOUSE 2A, ROCK ROAD, CAMBRIDGE
            "200004173004",  # 17 ROCK ROAD, CAMBRIDGE
            "10002571379",  # 122 HARTINGTON GROVE, CAMBRIDGE
            "200004186766",  # 198 QUEEN EDITHS WAY, CAMBRIDGE
            "10090966442",  # RIVERBOAT TUMBLING WATER G20635 RIVERSIDE, CAMBRIDGE
        ]:
            return None

        if record.housepostcode in [
            # splits
            "CB4 1LD",
            "CB2 4JF",
        ]:
            return None

        return super().address_record_to_dict(record)

    # Workaround to use coordinate data in Halarose file for mapping
    def get_station_point(self, record):
        x_coord = float(record.pollingstationeasting)
        y_coord = float(record.pollingstationnorthing)

        if x_coord > 0 and y_coord > 0:
            return Point(
                x_coord,
                y_coord,
                srid=27700,
            )

        return super().get_station_point(record)

    def station_record_to_dict(self, record):
        # More accurate point for station, awaiting council reply:
        # # The Salvation Army Community Centre, 104, Mill Road, Cambridge
        # if self.get_station_hash(record) == "28-the-salvation-army-community-centre":
        #     record = record._replace(
        #         pollingstationeasting="546177.25", pollingstationnorthing="257892.79"
        #     )

        return super().station_record_to_dict(record)
