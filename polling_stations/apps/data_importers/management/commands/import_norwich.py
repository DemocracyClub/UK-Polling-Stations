from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = (
        "2023-05-04/2023-04-21T13:20:24.756727/DC - Polling districts export.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-21T13:20:24.756727/DC - Polling stations export.csv"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # ST THOMAS PARISH HALL
        # https://wheredoivote.co.uk/admin/bug_reports/bugreport/576/change/
        if record.stationcode == "33NE2":
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)
