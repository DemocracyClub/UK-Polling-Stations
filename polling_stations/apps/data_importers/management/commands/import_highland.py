from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "HLD"
    addresses_name = (
        "2022-05-05/2022-03-24T15:19:09.669660/H Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-24T15:19:09.669660/H Democracy Club - Polling Stations.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.uprn in ["130131593"]:
            return None
        if record.postcode == "IV17 0QY":
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Coigach Community Hall, Achiltibuie
        if record.stationcode in ["W01 001", "W05 053"]:
            record = record._replace(xordinate="202914", yordinate="907677")
        return super().station_record_to_dict(record)
