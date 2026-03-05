from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SNO"
    addresses_name = "2026-05-07/2026-03-05T09:53:17.224658/South Norfolk Council Polling Districts.csv"
    stations_name = "2026-05-07/2026-03-05T09:53:17.224658/South Norfolk Council Polling Stations.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-8-sig"

    def address_record_to_dict(self, record):
        if record.uprn in [
            "2630126388",  # KIMBERLEY FARMS LTD, MANOR FARM, COSTON, NORWICH, NR9 4DT
        ]:
            return None

        if record.postcode in [
            # split
            "IP22 5UE",
            "NR14 7WH",
        ]:
            return None
        return super().address_record_to_dict(record)
