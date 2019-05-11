from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000087"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019fare.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019fare.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 == "SO31 1EY":
            rec["postcode"] = "SO311BY"
            rec["accept_suggestion"] = False

        return rec
