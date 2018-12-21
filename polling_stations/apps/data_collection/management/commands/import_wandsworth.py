from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000032"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.addressline6 == "SW16 6NN":
            return None
        if record.property_urn == "10090497135":
            return None
        if record.property_urn == "121034679":
            return None

        return super().address_record_to_dict(record)
