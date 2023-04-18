from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SHE"
    addresses_name = "2023-05-04/2023-04-18T10:57:30.072283/Polling District - Folkestone and Hythe (1).csv"
    stations_name = "2023-05-04/2023-04-18T10:57:30.072283/Polling Stations - Folkestone and Hythe.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "TN29 9AU",
            "TN28 8PW",
            "CT20 3RE",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.stationcode == "28":
            # Hawkinge Pavillion and Sports Ground
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)
