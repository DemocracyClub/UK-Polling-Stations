from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000028"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Carlisle.tsv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Carlisle.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6 == "CA1 2AQ":
            return None

        return super().address_record_to_dict(record)
