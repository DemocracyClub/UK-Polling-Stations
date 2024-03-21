from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STT"
    addresses_name = (
        "2024-05-02/2024-03-21T08:33:57.392759/Democracy_Club__02May2024 2.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-21T08:33:57.392759/Democracy_Club__02May2024 2.CSV"
    )
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # Mobile Polling Station, Grassed area to the side of The Merlin Pub, Marsh House Avenue, Billingham TS23 3SY
        if record.polling_place_id == "15366":
            record = record._replace(polling_place_postcode="TS23 3QJ")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "TS17 9PA",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
