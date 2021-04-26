from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERY"
    addresses_name = (
        "2021-04-16T11:19:35.745167/Democracy Club - Polling Districts PCC 2021.csv"
    )
    stations_name = (
        "2021-04-16T11:19:35.745167/Democracy Club - Polling Stations PCC 2021.csv"
    )
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10024434625",
            "10094489161",
            "100050024437",
        ]:
            return None
        return super().address_record_to_dict(record)
