from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FEN"
    addresses_name = "2024-07-04/2024-06-03T09:57:53.342984/Democracy Club FDC Polling Districts June 2024.csv"
    stations_name = "2024-07-04/2024-06-03T09:57:53.342984/Democracy Club FDC Polling Stations June 2024.csv"
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            "PE14 0LF",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
