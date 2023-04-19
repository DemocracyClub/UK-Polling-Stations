from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "AMB"
    addresses_name = "2023-05-04/2023-04-19T10:28:01.382651/18 04 23 District.csv"
    stations_name = (
        "2023-05-04/2023-04-19T10:28:01.382651/D C Polling Stations 2023.csv"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # ST.ANDREWS CHURCH HALL Station Road'
        if record.stationcode in ["CMS", "CME"]:
            record = record._replace(postcode="")

        if record.stationcode == "HAL":
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "10013426910",  # 21 DALBY GREEN CLOSE, WAINGROVES, RIPLEY
            "10013426909",  # 22 DALBY GREEN CLOSE, WAINGROVES, RIPLEY
        ]:
            return None
        return super().address_record_to_dict(record)
