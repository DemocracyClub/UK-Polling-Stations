from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WSM"
    addresses_name = (
        "2022-05-05/2022-03-04T15:30:07.536856/polling_station_export-2022-03-04.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-04T15:30:07.536856/polling_station_export-2022-03-04.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # Danubius Hotel
        if record.pollingstationnumber == "74":
            rec = super().station_record_to_dict(record)
            rec[
                "address"
            ] = "Danubius Hotel\n18 Lodge Road\n(Entrance on Park Road)\nSt John's Wood\nLondon"
            return rec

        # Seymour Leisure Centre
        if record.pollingstationnumber == "48":
            rec = super().station_record_to_dict(record)
            rec[
                "address"
            ] = "Seymour Leisure Centre\nSeymour Place\n(Entrance on Shouldham Street)\nLondon"
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10033552804",  # FLAT 3, 2 MORETON CLOSE, LONDON
            "10033618772",  # THIRD FLOOR 48 CHANDOS PLACE, LONDON
            "100022803552",  # 9 ST.BARNABAS STREET, LONDON
            "100022749688",  # 50 ELNATHAN MEWS, LONDON
        ]:
            return None

        if record.housepostcode in [
            "W1K 7JB",
            "W2 6PF",
            "SW1P 4JZ",
            "W1U 8BD",
            "NW8 8LH",
            "W10 4PR",
            "W2 5HA",
            "W9 3DW",
            "W9 2AL",
            "SW1V 4AF",
            "NW8 6DT",
            "NW8 6DU",
            "W1K 2HX",
        ]:
            return None

        return rec
