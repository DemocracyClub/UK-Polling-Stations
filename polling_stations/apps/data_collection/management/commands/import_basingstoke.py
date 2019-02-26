from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000084"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019.CSV02May2019.tsv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019.CSV02May2019.tsv"
    )
    elections = ["local.2019-05-02"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["100062463351"]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        return super().address_record_to_dict(record)
