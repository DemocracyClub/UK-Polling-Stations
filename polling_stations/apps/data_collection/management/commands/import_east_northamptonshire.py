from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000152"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019ENorth.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019ENorth.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10001197605":
            rec["postcode"] = "NN10 9XH"

        if uprn == "10090611778":
            rec["postcode"] = "NN144BD"
            rec["accept_suggestion"] = False

        if uprn in ["200000731079", "10001197785", "10001198047"]:
            rec["accept_suggestion"] = True

        return rec
