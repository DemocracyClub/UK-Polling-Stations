from data_importers.ems_importers import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STV"
    addresses_name = "2021-03-08T10:02:40.312121/Democracy Club - Polling Districts.csv"
    stations_name = "2021-03-08T10:02:40.312121/Democracy Club - Polling Stations.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.postcode == "SG1 4XS":
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # https://trello.com/c/5gWxFAJw/369-stevenage

        if record.placename == "JOINT EMERGENCY SERVICE ACADEMY":
            record = record._replace(xordinate="522946", yordinate="225975")

        if record.placename == "WESTON ROAD CEMETERY":
            record = record._replace(
                postcode="SG1 4DE", xordinate="524300", yordinate="226360"
            )

        return super().station_record_to_dict(record)
