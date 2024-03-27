from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRO"
    addresses_name = (
        "2024-05-02/2024-04-11T14:43:59.023504/BDC Democracy Club Polling Districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-04-11T14:43:59.023504/BDC Democracy Club Polling Stations.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip("0").strip()

        if uprn in [
            "10009923018",  # THE BUNGALOW, THE HEATH, HEVINGHAM, NORWICH
        ]:
            return None

        if record.postcode in [
            "NR7 0RY",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
