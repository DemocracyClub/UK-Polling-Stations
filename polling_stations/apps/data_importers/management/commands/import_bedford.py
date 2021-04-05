from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BDF"
    addresses_name = (
        "2021-03-17T12:11:37.989847/Bedford Polling Districts - Democracy Club.csv"
    )
    stations_name = (
        "2021-03-17T12:11:37.989847/Bedford Polling Stations for Democracy Club.csv"
    )
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        # KEMPSTON WEST METHODIST CHURCH Carried forward from local.2019-05-02
        if record.stationcode == "44":
            record = record._replace(xordinate="502614")
            record = record._replace(yordinate="247440")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if record.postcode in ["MK43 9AH"]:
            return None

        if uprn in ["100080991603"]:
            return None

        return super().address_record_to_dict(record)
