from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "WSM"
    addresses_name = "2026-05-07/2026-03-10T11:27:05.934023/Democracy Club - Idox_2026-03-10 10-57.csv"
    stations_name = "2026-05-07/2026-03-10T11:27:05.934023/Democracy Club - Idox_2026-03-10 10-57.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100022749688",  # 50 ELNATHAN MEWS, LONDON
            "10033529430",  # HYDE PARK BUCK HILL LODGE BAYSWATER ROAD, LONDON
            "100023382377",  # QUEENS GATE LODGE, HYDE PARK GATE, LONDON
            "10033641257",  # HOUSEBOAT WILLOW OPPOSITE 49 BLOMFIELD ROAD, LONDON
            "10033654811",  # BOATHOME LILA, BLOMFIELD ROAD, LONDON
            "10033622302",  # HOUSEBOAT DUENDE, BLOMFIELD ROAD, LONDON
            "10033649347",  # GROUND FLOOR FLAT 164 PORTNALL ROAD, LONDON
        ]:
            return None

        if record.postcode in [
            # split
            "NW8 8LH",
            "SW1P 4JZ",
            "SW1V 4AF",
            "W1K 7JB",
            "W2 5HA",
            "W9 2AL",
            "W9 3DW",
        ]:
            return None

        return super().address_record_to_dict(record)
