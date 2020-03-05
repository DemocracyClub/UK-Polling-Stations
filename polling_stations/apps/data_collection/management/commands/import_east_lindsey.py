from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000137"
    addresses_name = "2020-02-19T11:36:55.208138/Democracy_Club__07May2020.tsv"
    stations_name = "2020-02-19T11:36:55.208138/Democracy_Club__07May2020.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 in ["PE22 0TN", "PE220TW"]:
            return None

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "8585":
            record = record._replace(polling_place_easting="531703")
            record = record._replace(polling_place_northing="391688")

        return super().station_record_to_dict(record)
