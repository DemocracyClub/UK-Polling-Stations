from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000026"
    addresses_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018.CSV"
    stations_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018.CSV"
    elections = ["local.2018-05-03"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        # Point supplied for Chaddlewood Farm Community Centre is miles off
        if record.polling_place_id == "1197":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)
