from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000226"
    addresses_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Crawley supplied corrected grid refs by email
        if record.polling_place_id == "591":
            record = record._replace(polling_place_easting="526564")
            record = record._replace(polling_place_northing="135576")
        if record.polling_place_id == "571":
            record = record._replace(polling_place_easting="528408")
            record = record._replace(polling_place_northing="135808")
        return super().station_record_to_dict(record)
