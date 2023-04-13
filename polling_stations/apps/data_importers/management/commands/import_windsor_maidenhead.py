from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WNM"
    addresses_name = (
        "2023-05-04/2023-04-13T15:19:53.305902/democracy club polling districts.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-13T15:19:53.305902/democracy club polling stations.csv"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # Polling station A Mobile Unit at Waitrose Carpark
        if record.stationcode == "75WSC3":
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)
