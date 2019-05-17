from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000009"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Ealing.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Ealing.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn == "12180962":
            rec["postcode"] = "W13 8JP"

        return rec
