from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000149"
    addresses_name = "local.2019-05-02/Version 1/SouthNorfolk2019PollingStation Report for Democracy Club Website.csv"
    stations_name = "local.2019-05-02/Version 1/SouthNorfolk2019PollingStation Report for Democracy Club Website.csv"
    elections = ["local.2019-05-02"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "2630159192",
            "2630101566",
            "2630106361",
            "2630164300",
            "2630122694",
        ]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        if uprn == "2630153843":
            rec["postcode"] = "NR14 6RJ"
            rec["accept_suggestion"] = False
            return rec

        return rec
