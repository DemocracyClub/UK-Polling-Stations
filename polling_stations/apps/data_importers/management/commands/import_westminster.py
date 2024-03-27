from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WSM"
    addresses_name = "2024-05-02/2024-03-27T14:42:03.748146/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-27T14:42:03.748146/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10033552804",  # FLAT 3, 2 MORETON CLOSE, LONDON
            "10033618772",  # THIRD FLOOR 48 CHANDOS PLACE, LONDON
            "100022749688",  # 50 ELNATHAN MEWS, LONDON
            "10033529430",  # HYDE PARK BUCK HILL LODGE BAYSWATER ROAD, LONDON
            "100023382377",  # QUEENS GATE LODGE, HYDE PARK GATE, LONDON
        ]:
            return None

        if record.housepostcode in [
            # split
            "W2 5HA",
            "W2 6PF",
            "SW1P 4JZ",
            "NW8 8LH",
            "W1K 7JB",
            "W9 3DW",
            "W9 2AL",
            "SW1V 4AF",
        ]:
            return None

        return super().address_record_to_dict(record)
