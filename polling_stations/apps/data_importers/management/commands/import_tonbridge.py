from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TON"
    addresses_name = "2024-07-04/2024-06-24T13:00:52.040925/ton-combined.csv"
    stations_name = "2024-07-04/2024-06-24T13:00:52.040925/ton-combined.csv"
    elections = ["2024-07-04"]

    duplicate_stations = ["JUDD-31", "JUDD-32", "JUDD-33", "JUDD-34"]

    def station_record_to_dict(self, record):
        if record.pollingstationnumber in self.duplicate_stations:
            return None
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.pollingstationnumber in self.duplicate_stations:
            return None

        if record.housepostcode in [
            # split
            "ME20 6HZ",
            "TN11 0ES",
            "TN10 4JJ",
            "TN11 0AJ",
            "ME19 5PA",
        ]:
            return None
        return super().address_record_to_dict(record)
