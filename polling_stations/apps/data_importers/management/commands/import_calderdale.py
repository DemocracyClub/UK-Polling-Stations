from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CLD"
    addresses_name = "2022-05-05/2022-03-21T11:38:20.891364/Calderdale Polling Districts 2022 05 05.csv"
    stations_name = "2022-05-05/2022-03-21T11:38:20.891364/Calderdale Polling Stations 2022 05 05.csv"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if record.postcode == "OL14 6RS":
            return None
        if uprn in [
            "200001691811",
            "200001826572",
        ]:

            return None
        return super().address_record_to_dict(record)
