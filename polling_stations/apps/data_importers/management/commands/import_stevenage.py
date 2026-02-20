from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STV"
    addresses_name = "2026-05-07/2026-02-20T14:19:29.496548/SBC Polling Districts.csv"
    stations_name = "2026-05-07/2026-02-20T14:19:29.496548/SBC Polling Stations.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.uprn in [
            "10070255691",  # PHILBECK HOUSE, MAXWELL ROAD, STEVENAGE, SG1 2EP
            "10070258366",  # FLAT 3, NEWTON HOUSE, DANESTRETE, STEVENAGE, SG1 1WR
        ]:
            return None

        if record.postcode in [
            # looks wrong
            "SG1 1HE",
            "SG1 1AR",
        ]:
            return None

        return super().address_record_to_dict(record)
