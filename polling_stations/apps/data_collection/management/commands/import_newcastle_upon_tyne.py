from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000021"
    addresses_name = "local.2018-05-03/Version 3/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 3/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6.strip() == "NE16 6JE":
            return None

        if record.property_urn.strip() == "004510741266":
            return None

        return super().address_record_to_dict(record)
