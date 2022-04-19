from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FIF"
    addresses_name = (
        "2022-05-05/2022-04-19T11:25:34.787070/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-19T11:25:34.787070/Democracy Club - Polling Stations.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):

        if record.stationcode in [
            "176",  # MARKINCH TOWN HALL
            "177",  # MARKINCH TOWN HALL
            "178",  # MARKINCH TOWN HALL
            "229",  # BURNSIDE VILLAGE HALL
            "230",  # BURNSIDE VILLAGE HALL
        ]:
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            "KY1 2EZ",
            "KY5 9EY",
        ]:
            return None

        return super().address_record_to_dict(record)
