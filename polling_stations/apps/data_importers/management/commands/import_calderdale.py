from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CLD"
    addresses_name = "2021-04-16T12:55:22.326313/CMBC Polling Districts.csv"
    stations_name = "2021-04-16T12:55:22.326313/CMBC Polling Stations.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "200001826572":
            return None
        return super().address_record_to_dict(record)
