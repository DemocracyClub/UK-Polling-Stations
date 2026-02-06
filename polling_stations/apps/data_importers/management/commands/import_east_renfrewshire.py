from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERW"
    addresses_name = (
        "2026-05-07/2026-02-06T14:50:06.403472/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2026-05-07/2026-02-06T14:50:06.403472/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "G46 7JL",
        ]:
            return None

        return super().address_record_to_dict(record)
