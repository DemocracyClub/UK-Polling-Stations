from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FEN"
    addresses_name = "2023-05-04/2023-04-30T20:24:10.048671/Democracy Club FDC Polling Districts May 2023.csv"
    stations_name = "2023-05-04/2023-04-30T20:24:10.048671/Democracy Club FDC Polling Stations May 2023.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "PE14 0LF",
        ]:
            return None

        return super().address_record_to_dict(record)
