from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000011"
    addresses_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018 UPDATED.tsv"
    stations_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018 UPDATED.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.property_urn == "10000159530":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "PE28 2UD"
            return rec

        return super().address_record_to_dict(record)
