from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SCB"
    addresses_name = (
        "2024-07-04/2024-06-19T09:53:02.169391/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-19T09:53:02.169391/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "TD6 0EB",
            "TD1 3NY",
        ]:
            return None
        if record.uprn in [
            "116074488",
            "116095151",
            "116054256",
        ]:
            return None
        return super().address_record_to_dict(record)
