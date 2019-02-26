from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000035"
    addresses_name = "local.2019-05-02/Version 2/DerbyDalesDC polling districts.csv"
    stations_name = "local.2019-05-02/Version 2/DerbyDalesDC polling stations.csv"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in ["10010331972", "10010331834", "10070090689"]:
            rec["accept_suggestion"] = True

        return rec
