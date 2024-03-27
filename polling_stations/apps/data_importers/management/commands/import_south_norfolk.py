from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SNO"
    addresses_name = (
        "2024-05-02/2024-04-05T12:50:53.885247/SNC Democracy Club Polling Districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-04-05T12:50:53.885247/SNC Democracy Club Polling Stations.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            "IP22 5UE",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
