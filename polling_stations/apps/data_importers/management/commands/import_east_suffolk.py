from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ESK"
    addresses_name = (
        "2021-03-31T14:17:43.933405/East Suffolk Council Area - Polling Districts.csv"
    )
    stations_name = "2021-03-31T14:17:43.933405/East Suffolk Council Area - Polling Stations - v2.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.stationcode in ("12", "12X", "12XX", "12XXX"):
            # Shadingfield Village Hall
            record = record._replace(postcode="NR34 8DH")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in ["NR35 1BZ", "IP12 2SY", "NR32 4ER"]:
            return None  # split

        return super().address_record_to_dict(record)
