from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "REI"
    addresses_name = "2022-05-05/2022-04-08T09:12:49.913080/RBBC Polling Districts.csv"
    stations_name = "2022-05-05/2022-04-08T09:12:49.913080/RBBC Polling Stations.csv"
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # Woodmansterne Village Hall, Carshalton Road, Woodmansterne, Banstead, Surrey
        if record.stationcode == "CKW1":
            record = record._replace(xordinate="527572", yordinate="160117")

        # St John`s Church Hall, The Avenue, Tadworth, Surrey
        if record.stationcode in ["KTW1.1", "KTW1.2"]:
            record = record._replace(postcode="KT20 5DB")  # was KT20 5AB

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip("0")

        if uprn in [
            "68176955",  # 1 PUTNEY CROFY, HORLEY
            "68176948",  # 2 PUTNEY CROFY, HORLEY
            "68181592",  # 2A PARKHURST ROAD, HORLEY
        ]:
            return None

        return super().address_record_to_dict(record)
