from data_importers.management.commands import BaseHalaroseCsvImporter


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

        return super().station_record_to_dict(record)
