from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STV"
    addresses_name = (
        "2022-05-05/2022-03-16T14:30:37.871583/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-16T14:30:37.871583/Democracy Club - Polling Stations.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # https://trello.com/c/5gWxFAJw/369-stevenage

        if record.placename == "JOINT EMERGENCY SERVICE ACADEMY":
            record = record._replace(xordinate="522946", yordinate="225975")

        if record.placename == "WESTON ROAD CEMETERY":
            record = record._replace(
                postcode="SG1 4DE", xordinate="524300", yordinate="226360"
            )

        return super().station_record_to_dict(record)
