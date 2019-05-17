from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000016"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019haver.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019haver.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # File supplied contained obviously inaccurate point
        # Replace with correction from council
        if record.polling_place_id == "7687":
            record = record._replace(polling_place_easting="550712.13")

        return super().station_record_to_dict(record)
