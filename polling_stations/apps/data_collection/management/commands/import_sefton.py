from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000014"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 == "L20 9AH":
            return None

        if record.addressline6 == "L37 7AQ":
            return None

        if record.addressline6 == "L20 6EA":
            return None

        if record.addressline6 == "PR9 9JH":
            return None

        if record.addressline6 == "L20 5AB":
            return None

        if record.addressline6 == "L38 7JB":
            return None

        return super().address_record_to_dict(record)
