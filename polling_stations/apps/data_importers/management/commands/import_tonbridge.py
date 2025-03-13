from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TON"
    addresses_name = (
        "2025-05-01/2025-03-13T12:57:10.156992/Tonbridge & Malling data.csv"
    )
    stations_name = "2025-05-01/2025-03-13T12:57:10.156992/Tonbridge & Malling data.csv"
    elections = ["2025-05-01"]

    def station_record_to_dict(self, record):
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "ME20 6HZ",
            "TN11 0AJ",
            "ME19 5PA",
            "TN10 4JJ",
            "TN11 0ES",
        ]:
            return None

        return super().address_record_to_dict(record)
