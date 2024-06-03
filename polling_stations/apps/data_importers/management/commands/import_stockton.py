from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STT"
    addresses_name = (
        "2024-07-04/2024-06-03T14:23:57.541993/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-03T14:23:57.541993/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # Mobile Polling Station, Grassed area to the side of The Merlin Pub, Marsh House Avenue, Billingham TS23 3SY
        if record.polling_place_id == "15826":
            record = record._replace(polling_place_postcode="TS23 3QJ")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "TS17 9PA",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
