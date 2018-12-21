from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000089"
    addresses_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "2115":
            record = record._replace(polling_place_easting="479224")
            record = record._replace(polling_place_northing="154016")

        if record.polling_place_id == "2338":
            record = record._replace(polling_place_easting="481347")
            record = record._replace(polling_place_northing="160855")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6 == "RG27 9QP":
            return None

        return super().address_record_to_dict(record)
