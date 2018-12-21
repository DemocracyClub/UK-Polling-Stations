from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000017"
    addresses_name = (
        "local.2018-05-03/Version 1/Democracy_Club__03May2018 (3) Hillingdon.tsv"
    )
    stations_name = (
        "local.2018-05-03/Version 1/Democracy_Club__03May2018 (3) Hillingdon.tsv"
    )
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10090329328":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "UB4 9LW"
            return rec

        if uprn == "10092980468":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "UB8 3PF"
            return rec

        if uprn in ["10092982613", "10092982616", "10092982617"]:
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "UB4 0SE"
            return rec

        if uprn == "10022797188":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "UB8 1UJ"
            return rec

        if uprn == "10009948891":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "UB4 0RJ"
            return rec

        if uprn == "10022805692":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "UB10 0BQ"
            return rec

        return super().address_record_to_dict(record)
