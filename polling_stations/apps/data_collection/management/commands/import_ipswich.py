from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000202"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Ipswich.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Ipswich.CSV"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["100091636692", "10093555116", "100091482960"]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        return super().address_record_to_dict(record)
