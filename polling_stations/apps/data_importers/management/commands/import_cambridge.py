from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "CAB"
    addresses_name = "2024-05-02/2024-03-18T15:24:22.305713/Eros_SQL_Output015.csv"
    stations_name = "2024-05-02/2024-03-18T15:24:22.305713/Eros_SQL_Output015.csv"
    elections = ["2024-05-02"]

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
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: The Salvation Army Community Centre, 104, Mill Road, Cambridge, CB1 2DB
        if record.pollingstationnumber == "36":
            record = record._replace(pollingstationpostcode="CB1 2BD")

        # coords correction for: St. Andrew's Hall,97 St. Andrew's Road, Cambridge, CB4 1DH
        if record.pollingstationnumber == "21":
            record = record._replace(
                pollingstationeasting="546314", pollingstationnorthing="259588"
            )

        return super().station_record_to_dict(record)

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
