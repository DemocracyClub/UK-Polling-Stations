from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ECA"
    addresses_name = (
        "2021-03-26T11:32:58.058350/Democracy Club - polling Districts 2021 V2.csv"
    )
    stations_name = (
        "2021-03-26T11:32:58.058350/Democracy Club - Polling Stations 2021 V2.csv"
    )
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):

        if record.stationcode == "LE1":
            # KENNETT PAVILION
            record = record._replace(postcode="CB8 7QF")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if record.stationcode in [
            "COV17/1",
            "NEW43/1",
            "NEW44/1",
        ]:
            return None
        if uprn in ["10002611549"]:
            return None

        return super().address_record_to_dict(record)
