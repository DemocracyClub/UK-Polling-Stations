from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000011"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019hunt.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019hunt.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "6265":  # Berkley Street Methodist Church
            record = record._replace(polling_place_postcode="PE19 2NB")

        return super().station_record_to_dict(record)
