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

        if uprn == "10001344107":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "NG15 8JA"
            return rec

        if uprn == "10001337112":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "NG17 4FU"
            return rec

        if uprn == "10001342248":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "NG17 1FU"
            return rec

        if uprn == "10070852165":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "NG17 8HS"
            return rec

        return super().address_record_to_dict(record)
