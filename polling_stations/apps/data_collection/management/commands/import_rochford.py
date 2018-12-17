from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000075"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Rochford.CSV"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Rochford.CSV"
    elections = ["local.2018-05-03"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):

        # All of the UPRN data from Rochford is a bit dubious.
        # For safety I'm just going to ignore them all
        record = record._replace(property_urn="")

        bad_postcodes = ["SS6 8RJ", "SS9 5AE"]

        if record.addressline6.strip() in bad_postcodes:
            return None

        return super().address_record_to_dict(record)
