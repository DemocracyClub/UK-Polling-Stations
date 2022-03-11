from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STY"
    addresses_name = (
        "2022-05-05/2022-03-11T15:09:17.360297/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-11T15:09:17.360297/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Cleadon Park Health Centre, Polling Station A
        # Cleadon Park Health Centre, Polling Station B
        # *PLEASE USE PRINCE EDWARD ROAD ENTRANCE*
        # Change coords to make maps right
        if record.polling_place_id in ["3586", "3699"]:
            record = record._replace(polling_place_easting="437517")
            record = record._replace(polling_place_northing="564289")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in ["NE31 2XF", "NE34 8AE"]:
            return None

        return super().address_record_to_dict(record)
