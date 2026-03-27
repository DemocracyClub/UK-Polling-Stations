from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRO"
    addresses_name = "2026-05-07/2026-03-25T11:56:45.972737/Broadland District Council Polling Districts.csv"
    stations_name = "2026-05-07/2026-03-25T11:56:45.972737/Broadland District Council Polling Stations.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            # looks wrong
            "NR13 6DB",
        ]:
            return None
        return super().address_record_to_dict(record)
