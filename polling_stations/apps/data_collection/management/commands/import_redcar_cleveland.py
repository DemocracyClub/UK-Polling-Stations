from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000003"
    addresses_name = "local.2019-05-02/Version 3/Democracy_Club__02May2019Redar.tsv"
    stations_name = "local.2019-05-02/Version 3/Democracy_Club__02May2019Redar.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100110675731":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "TS134EA"
            return rec

        if uprn == "10034518861":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "TS79LF"
            return rec

        if uprn == "10023906866":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "TS9 6QR"
            return rec

        if uprn == "10034529574":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "TS11 7HP"
            return rec

        return super().address_record_to_dict(record)
