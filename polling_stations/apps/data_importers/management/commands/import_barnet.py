from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = "2024-07-04/2024-06-17T11:08:27.771011/BNE_districts_combined.csv"
    stations_name = "2024-07-04/2024-06-17T11:08:27.771011/BNE_stations_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093301425",  # FLAT 1, 15 COLLISON AVENUE, BARNET
            "200001537",  # 1 ABERCORN CLOSE, LONDON
            "10095744883",  # 5 EGRET SQUARE, LONDON
        ]:
            return None
        if record.postcode in [
            # split
            "EN5 3DP",
            "N12 7LT",
        ]:
            return None
        return super().address_record_to_dict(record)
