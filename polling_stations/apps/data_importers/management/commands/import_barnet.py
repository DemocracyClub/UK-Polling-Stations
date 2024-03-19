from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = "2024-05-02/2024-03-26T15:58:39.559553/Democracy Club data.csv"
    stations_name = (
        "2024-05-02/2024-03-26T15:58:39.559553/Democracy Club Polling Station data.csv"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093301425",  # FLAT 1, 15 COLLISON AVENUE, BARNET
            "200001537",  # 1 ABERCORN CLOSE, LONDON
        ]:
            return None
        if record.postcode in [
            "EN5 3DP",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
