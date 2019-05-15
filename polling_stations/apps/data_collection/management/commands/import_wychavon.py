from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000238"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019.csv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019.csv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["100120707960", "100120707957", "100120716820"]:
            rec["accept_suggestion"] = True

        if uprn in ["10013941784"]:
            rec["accept_suggestion"] = False

        return rec
