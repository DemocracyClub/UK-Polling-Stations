from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000229"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019worthing.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019worthing.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 in ["BN11 2FL", "BN11 2FJ"]:
            rec["accept_suggestion"] = False

        return rec
