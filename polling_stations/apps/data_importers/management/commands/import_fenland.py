from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FEN"
    addresses_name = (
        "2024-05-02/2024-03-19T11:49:39.152620/Dem Club Polling Districts May 2024.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-19T11:49:39.152620/Dem Club Polling Stations May 2024.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            "PE14 0LF",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
