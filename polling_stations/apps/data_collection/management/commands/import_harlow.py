from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000073"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Harlow.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Harlow.CSV"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200002566340"  # CM179LU -> CM179DS : The Farmhouse, London Road, Harlow, Essex
        ]:
            rec["accept_suggestion"] = False

        return rec
