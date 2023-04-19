from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DEB"
    addresses_name = "2023-05-04/2023-04-19T10:30:20.449617/Democracy Club - Polling Districts 170423.csv"
    stations_name = "2023-05-04/2023-04-19T10:30:20.449617/Democracy Club - Polling Stations 180423.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "DE6 2AR",
        ]:
            return None

        return super().address_record_to_dict(record)
