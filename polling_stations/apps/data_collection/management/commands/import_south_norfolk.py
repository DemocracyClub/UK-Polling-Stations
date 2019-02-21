from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000149"
    addresses_name = "local.2019-05-02/Version 1/SouthNorfolk2019PollingStation Report for Democracy Club Website.csv"
    stations_name = "local.2019-05-02/Version 1/SouthNorfolk2019PollingStation Report for Democracy Club Website.csv"
    elections = ["local.2019-05-02"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.property_urn.strip().lstrip("0") == "2630166893":
            rec["postcode"] = "NR9 3JP"

        if record.property_urn.strip().lstrip("0") == "2630159192":
            rec["postcode"] = "NR35 2QR"

        if record.property_urn.strip().lstrip("0") == "2630153843":
            rec["postcode"] = "NR14 6RJ"

        return rec
