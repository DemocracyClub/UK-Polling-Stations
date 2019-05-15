from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000084"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019basing.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019basing.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn == "10008485351":
            rec["postcode"] = "RG26 5HL"

        if uprn in ["100062463351"]:
            rec["accept_suggestion"] = True

        return rec
