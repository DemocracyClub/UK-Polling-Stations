from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERW"
    addresses_name = (
        "2024-07-04/2024-06-06T09:13:28.285718/Democracy Counts - Polling Districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-06T09:13:28.285718/Democracy Counts - Polling Stations.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "G46 7JL",
            "G76 8RW",
        ]:
            return None

        return super().address_record_to_dict(record)
