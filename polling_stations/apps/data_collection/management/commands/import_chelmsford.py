from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000070"
    addresses_name = "parl.2019-12-12/Version 2/merged.tsv"
    stations_name = "parl.2019-12-12/Version 2/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

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

        if record.addressline6.strip() == "CM1 1PJ":
            return None

        if uprn in [
            "10091492809"  # CM11LA -> CM111LA : 2 The Paddocks, Layland Farm, Sudbury Road, Downham, Billericay, Essex
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100091234373"  # CM11AG -> CM35QY : 99 Watson Heights, Chelmsford, Essex
        ]:
            rec["accept_suggestion"] = False

        return rec
