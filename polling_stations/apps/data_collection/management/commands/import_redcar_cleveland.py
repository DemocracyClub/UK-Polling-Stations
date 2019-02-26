from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000003"
    addresses_name = "local.2019-05-02/Version 3/Democracy_Club__02May2019Redar.tsv"
    stations_name = "local.2019-05-02/Version 3/Democracy_Club__02May2019Redar.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034518861",
            "100110675731",
            "200002523561",
            "10023902772",
            "10023902773",
            "200002523768",
            "200002523076",
        ]:
            rec["accept_suggestion"] = True

        if uprn in ["10023906550"]:
            rec["accept_suggestion"] = False

        return rec
