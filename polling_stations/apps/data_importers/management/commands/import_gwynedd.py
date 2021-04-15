from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GWN"
    addresses_name = (
        "2021-03-29T13:05:21.699264/Gwynedd polling_station_export-2021-03-29.csv"
    )
    stations_name = (
        "2021-03-29T13:05:21.699264/Gwynedd polling_station_export-2021-03-29.csv"
    )
    elections = ["2021-05-06"]
    csv_encoding = "windows-1252"

    # > WARNING: Polling station 142-neuadd-bentref-aberangell is in Powys County
    # > (POW) Council but target council is Gwynedd Council (GWN) - manual check
    # > recommended
    #
    # Checked; actual village hall is within Aberangell, on the right side of the
    # boundary.

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "LL57 4HG",
            "LL55 4BT",
            "LL55 2SG",
            "LL54 7BN",
            "LL54 7UB",
            "LL57 3YF",
            "LL57 2NZ",
            "LL53 5TP",
            "LL53 8NH",
            "LL53 5AG",
            "LL53 8BL",
            "LL53 7TP",
            "LL53 8DR",
            "LL23 7LE",
            "LL36 9LF",
            "LL48 6AY",
            "LL41 3PW",
        ]:
            return None  # split

        if record.uprn in ["10024095703"]:
            return None  # suspicious distance

        return super().address_record_to_dict(record)
