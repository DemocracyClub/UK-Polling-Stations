from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000035"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "72740327":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "LS14 2EZ"
            return rec

        if uprn == "72034142":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "LS18 4HN"
            return rec

        return super().address_record_to_dict(record)
