from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNS"
    addresses_name = "2023-05-04/2023-04-13T15:16:58.037951/Polling Districts.csv"
    stations_name = "2023-05-04/2023-04-13T15:16:58.037951/Polling Stations.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "2007020712",
            "2007021402",
        ]:
            return None

        return super().address_record_to_dict(record)
