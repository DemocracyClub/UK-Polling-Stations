from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000070"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019chelm.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019chelm.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100091430409":
            rec["postcode"] = "CM111HZ"
            rec["accept_suggestion"] = False

        if uprn == "200004627070":
            rec["postcode"] = "CM6 3XD"

        if uprn == "100091237355":
            rec["postcode"] = "SS11 7DS"

        if uprn in [
            "10091492809"  # CM11LA -> CM111LA : 2 The Paddocks, Layland Farm, Sudbury Road, Downham, Billericay, Essex
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100091234373"  # CM11AG -> CM35QY : 99 Watson Heights, Chelmsford, Essex
        ]:
            rec["accept_suggestion"] = False

        return rec
