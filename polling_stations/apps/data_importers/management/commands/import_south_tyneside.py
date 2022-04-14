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
        # All fixes from Council
        # Cleadon Park Health Centre, Polling Station A
        # Cleadon Park Health Centre, Polling Station B
        # *PLEASE USE PRINCE EDWARD ROAD ENTRANCE*
        # Change coords to make maps right
        if record.polling_place_id in ["3586", "3699"]:
            record = record._replace(polling_place_easting="437517")
            record = record._replace(polling_place_northing="564289")

        # Mortimer Community Centre, Polling Station B
        if record.polling_place_id == "3701":
            record = record._replace(polling_place_easting="436749")
            record = record._replace(polling_place_northing="565333")

        # West Boldon Primary School, Polling Station B
        if record.polling_place_id == "3702":
            record = record._replace(polling_place_easting="435412")
            record = record._replace(polling_place_northing="561508")

        # Scout Hut, Polling Station B, Rear of Grey Horse Pub
        if record.polling_place_id == "3706":
            record = record._replace(polling_place_easting="436472")
            record = record._replace(polling_place_northing="561331")

        # St Josephs Community Hall, Polling Station B
        if record.polling_place_id == "3704":
            record = record._replace(polling_place_easting="433025")
            record = record._replace(polling_place_northing="562375")

        #  Primrose Community Centre, Polling Station B
        if record.polling_place_id == "3703":
            record = record._replace(polling_place_easting="432889")
            record = record._replace(polling_place_northing="563590")

        #  Territorial Army (TA) Centre, Entrance off Highfield Road next to Callum Drive
        if record.polling_place_id == "3694":
            record = record._replace(polling_place_easting="438015")
            record = record._replace(polling_place_northing="565762")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in ["NE31 2XF", "NE34 8AE"]:
            return None

        return super().address_record_to_dict(record)
