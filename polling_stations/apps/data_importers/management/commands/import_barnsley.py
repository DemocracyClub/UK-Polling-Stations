from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNS"
    addresses_name = (
        "2022-05-05/2022-03-25T09:18:02.587996/Democracy Club Polling Districts.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-25T09:18:02.587996/Democracy Club Polling Stations.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # TEMPORARY BUILDING AT GRASMERE CRESCENT
        if record.stationcode == "24":
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "2007020712",
            "2007021402",
        ]:
            return None

        return super().address_record_to_dict(record)
