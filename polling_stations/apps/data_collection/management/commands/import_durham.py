from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000047"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Durham.CSV"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Durham.CSV"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10000806992":
            rec["postcode"] = "DH8 9UN"

        return rec
