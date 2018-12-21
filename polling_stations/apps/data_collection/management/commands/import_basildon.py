from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000066"
    addresses_name = (
        "local.2018-05-03/Version 4/Democracy_Club__03May2018 (2)Basildon.tsv"
    )
    stations_name = (
        "local.2018-05-03/Version 4/Democracy_Club__03May2018 (2)Basildon.tsv"
    )
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10013353921":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "SS16 5PW"
            return rec

        if record.addressline6 == "CM11 2JX":
            return None

        if uprn == "10093026696":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "CM12 9TJ"
            return rec

        if record.addressline6 == "SS15 6SS":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "SS15 5SS"
            return rec

        if uprn == "10090450942":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "SS12 9LA"
            return rec

        return super().address_record_to_dict(record)
