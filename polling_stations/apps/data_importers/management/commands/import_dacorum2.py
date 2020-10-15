from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000096"
    addresses_name = "2020-02-03T10:27:29.701109/Democracy_Club__07May2020Dacorum.CSV"
    stations_name = "2020-02-03T10:27:29.701109/Democracy_Club__07May2020Dacorum.CSV"
    elections = ["2020-05-07"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        if record.polling_place_id == "1297":
            record = record._replace(polling_place_easting="507211")
            record = record._replace(polling_place_northing="204366")

        return super().station_record_to_dict(record)
