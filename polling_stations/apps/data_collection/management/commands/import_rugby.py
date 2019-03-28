from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000220"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019ruggers.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019ruggers.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10010524278":
            rec["postcode"] = "CV7 9LX"

        if uprn in [
            "100070189342"  # CV227JT -> CV227JS : 83 Lawford Lane, Bilton, Rugby
        ]:
            rec["accept_suggestion"] = False

        return rec
