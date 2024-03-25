from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ECA"
    addresses_name = "2024-05-02/2024-03-25T16:59:04.074992/Democracy Club - Polling Districts 2024.csv"
    stations_name = "2024-05-02/2024-03-25T16:59:04.074992/Polling Stations 2024.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "100090041333",  # 15 BLACK BANK ROAD, LITTLE DOWNHAM, ELY
            "100090041332",  # 17 BLACK BANK ROAD, LITTLE DOWNHAM, ELY
            "10095400067",  # 163 THE STREET, KIRTLING, NEWMARKET
        ]:
            return None

        return super().address_record_to_dict(record)
