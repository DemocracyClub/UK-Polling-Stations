from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "TEN"
    addresses_name = "2026-05-07/2026-03-19T10:47:08.499497/Democracy Club - Polling Districts 2026.csv"
    stations_name = "2026-05-07/2026-03-19T10:47:08.499497/Democracy Club - Polling Stations 2026.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if (
            record.uprn
            in [
                "10007943316",  # 48 NEW HALL LODGE PARK LOW ROAD, DOVERCOURT
                "100090634997",  # 366A MAIN ROAD, HARWICH
                "10096724996",  # SWEET PEA, MILL LANE, THORPE-LE-SOKEN, CLACTON-ON-SEA
                "100091268553",  # 163 MEADOW VIEW PARK, ST. OSYTH ROAD, LITTLE CLACTON, CLACTON-ON-SEA
            ]
        ):
            return None

        if record.postcode in [
            # split
            "CO13 0FZ",
            # suspect
            "CO15 1HX",
        ]:
            return None

        return super().address_record_to_dict(record)
