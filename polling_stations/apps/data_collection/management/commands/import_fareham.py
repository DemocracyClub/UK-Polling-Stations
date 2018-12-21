from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000087"
    addresses_name = (
        "local.2018-05-03/Version 2/Democracy_Club__03May2018 Fareham 2.tsv"
    )
    stations_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018 Fareham 2.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10012133107":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "PO15 7LR"
            return rec

        return super().address_record_to_dict(record)
