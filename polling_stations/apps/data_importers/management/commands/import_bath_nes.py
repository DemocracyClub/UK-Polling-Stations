from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BAS"
    addresses_name = "2024-07-04/2024-06-21T14:41:21.417224/BAS_combined_v3.csv"
    stations_name = "2024-07-04/2024-06-21T14:41:21.417224/BAS_combined_v3.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10094952037",  # KINGSHILL FARM, BRISTOL ROAD, COMPTON MARTIN, BRISTOL
            "100120029109",  # 15 UPPER BLOOMFIELD ROAD, BATH
            "10093714965",  # THE STABLE, GIBBET LANE, BRISTOL
        ]:
            return None

        if record.housepostcode in [
            # split
            "BA2 6DR",
            "BA2 5AD",
            "BA2 2RZ",
            # suspect
            "BA3 5SF",
        ]:
            return None
        return super().address_record_to_dict(record)
