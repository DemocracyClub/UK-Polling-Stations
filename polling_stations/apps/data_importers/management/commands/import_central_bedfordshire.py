from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CBF"
    addresses_name = (
        "2024-05-02/2024-03-05T14:33:07.893624/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-05T14:33:07.893624/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            "MK17 9QG",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
