from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "VGL"
    addresses_name = (
        "2024-07-04/2024-06-06T10:32:09.163599/polling-districts-combined.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-06T10:32:09.163599/polling-stations-combined.csv"
    )
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # bug report #683: postcode correction confirmed by council for:
        # HEBRON CHURCH ANNEXE - STATION A, PILL STREET, COGAN, PENARTH, VALE OF GLAMORGAN
        if record.stationcode == "14-a":
            record = record._replace(postcode="CF64 2JS")

        return super().station_record_to_dict(record)
