from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ECA"
    addresses_name = (
        "2021-03-04T16:04:21.709479/Democracy Club - Polling Districts 2021.csv"
    )
    stations_name = (
        "2021-03-04T16:04:21.709479/Democracy club - Polliong Stations 2021.csv"
    )
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):

        if record.stationcode == "LE1":
            # KENNETT PAVILION
            record = record._replace(postcode="CB8 7QF")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in ["10002611549"]:
            return None

        return super().address_record_to_dict(record)
