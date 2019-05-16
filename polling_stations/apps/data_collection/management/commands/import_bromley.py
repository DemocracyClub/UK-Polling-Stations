from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000006"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019brom.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019brom.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):

        if record.addressline6 == "BR7 6HL":
            return None

        return super().address_record_to_dict(record)
