from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BEN"
    addresses_name = (
        "2022-05-05/2022-03-22T16:39:49.511741/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-22T16:39:49.511741/Democracy Club - Polling Stations.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # St Mary's Willesden Parish Church, Neasden Lane, London
        if record.stationcode == "RW4_1":
            record = record._replace(yordinate="184797")
            record = record._replace(xordinate="521445")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "202228638",  # long way from rest of postcode
            "202053053",
            "202053054",
        ]:
            return None

        return super().address_record_to_dict(record)
