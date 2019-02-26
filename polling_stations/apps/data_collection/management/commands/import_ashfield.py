from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000170"
    addresses_name = (
        "local.2019-05-02/Version 2/Democracy_Club__02May2019(REVISED)Ashf.tsv"
    )
    stations_name = (
        "local.2019-05-02/Version 2/Democracy_Club__02May2019(REVISED)Ashf.tsv"
    )
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["100031234554", "100031241226", "10001342248", "10070852165"]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        return super().address_record_to_dict(record)
