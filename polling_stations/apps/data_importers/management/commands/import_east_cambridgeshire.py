from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ECA"
    addresses_name = (
        "2023-05-04/2023-04-28T10:26:41.812261/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-28T10:26:41.812261/Democracy Club - Polling Stations.csv"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if record.postcode in [
            # split
            "CB6 2SG",
        ]:
            return None
        if uprn in [
            "100090041333",  # 15 BLACK BANK ROAD, LITTLE DOWNHAM, ELY
            "100090041332",  # 17 BLACK BANK ROAD, LITTLE DOWNHAM, ELY
        ]:
            return None

        return super().address_record_to_dict(record)
