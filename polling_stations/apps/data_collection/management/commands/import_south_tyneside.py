from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000023"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019sts.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019sts.tsv"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100000345804":
            return None

        if uprn in [
            "200000002007"  # NE340PW -> NE340YE : Staff Residence, 169 Harton Lane, South Shields
        ]:
            rec["accept_suggestion"] = True

        return rec
