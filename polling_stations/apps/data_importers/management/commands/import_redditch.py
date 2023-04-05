from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RED"
    addresses_name = (
        "2023-05-04/2023-04-05T11:22:08.304289/Redditch Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-04-05T11:22:08.304289/Redditch Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # Matchborough Meeting Rooms Clifton Close Off Breaches Lane Redditch
        if record.polling_place_id == "7688":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)
