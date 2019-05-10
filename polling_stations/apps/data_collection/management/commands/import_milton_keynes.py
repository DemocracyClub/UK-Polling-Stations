from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000042"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019MK.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019MK.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "7179":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
        if record.polling_place_id == "7258":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6.strip() == "MK10 7JD":
            return None

        return super().address_record_to_dict(record)
