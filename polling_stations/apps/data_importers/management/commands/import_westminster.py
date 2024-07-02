from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WSM"
    addresses_name = "2024-07-04/2024-07-02T11:47:40.424979/WSM_combined_v2.csv"
    stations_name = "2024-07-04/2024-07-02T11:47:40.424979/WSM_combined_v2.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10033552804",  # FLAT 3, 2 MORETON CLOSE, LONDON
            "10033618772",  # THIRD FLOOR 48 CHANDOS PLACE, LONDON
            "100022749688",  # 50 ELNATHAN MEWS, LONDON
            "10033529430",  # HYDE PARK BUCK HILL LODGE BAYSWATER ROAD, LONDON
            "100023382377",  # QUEENS GATE LODGE, HYDE PARK GATE, LONDON
            "10033641257",  # HOUSEBOAT WILLOW OPPOSITE 49 BLOMFIELD ROAD, LONDON
            "10033575787",  # UPPER PENTHOUSE FLAT 12 PARK STREET, LONDON
            "10033575789",  # LOWER PENTHOUSE FLAT 12 PARK STREET, LONDON
        ]:
            return None

        if record.housepostcode in [
            # split
            "W2 5HA",
            "W1K 7JB",
            "W2 6PF",
            "SW1P 4JZ",
            "SW1V 4AF",
            "W9 3DW",
            "W9 2AL",
            "NW8 8LH",
        ]:
            return None

        return super().address_record_to_dict(record)
