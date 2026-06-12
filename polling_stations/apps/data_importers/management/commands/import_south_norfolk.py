from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SNO"
    addresses_name = "2026-07-16/2026-06-12T15:11:13.982321/South Norfolk Council - polling districts.csv"
    stations_name = "2026-07-16/2026-06-12T15:11:13.982321/South Norfolk Council - polling stations.csv"
    elections = ["2026-07-16"]
    csv_encoding = "utf-16le"

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
