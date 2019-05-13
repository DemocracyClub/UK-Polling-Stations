from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000151"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019daven.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019daven.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "28052662":
            rec["postcode"] = "NN113QJ"

        return rec
