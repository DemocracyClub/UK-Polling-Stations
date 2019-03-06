from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000041"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Woke.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Woke.CSV"
    elections = []
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in ["RG7 1ZE", "RG7 1ZG"]:
            rec["postcode"] = "RG7 1FQ"

        if uprn in ["14020309"]:
            rec["accept_suggestion"] = True

        if uprn in ["14059977"]:
            rec["accept_suggestion"] = False

        return rec
