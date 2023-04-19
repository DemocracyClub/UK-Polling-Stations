from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CBF"
    addresses_name = (
        "2023-05-04/2023-04-19T15:46:39.334042/Democracy Club - polling districts2.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-19T15:46:39.334042/polling stations for Democracy Club2.csv"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # Flitton Church Hall Brook Lane Flitton Beds MK45 5EJ - removing misleading point
        if record.stationcode == "Bx178WF-G1":
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "MK17 9QG",
        ]:
            return None

        return super().address_record_to_dict(record)
