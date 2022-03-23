from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOC"
    addresses_name = (
        "2022-05-05/2022-03-23T15:20:31.665075/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-23T15:20:31.665075/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # Polling Station G1, Medway Community Centre, 16 Medway Road, Worcester
        # first digit of easting typoed (2... -> 3...)
        if record.polling_place_id == "6146":
            record = record._replace(polling_place_easting="386430")

        # Polling Station 3 Main Hall, Woodgreen Church, Hastings Drive, Worcester
        # first digit of easting typoed (2... -> 3...)
        if record.polling_place_id == "6262":
            record = record._replace(polling_place_easting="388009")

        return super().station_record_to_dict(record)
