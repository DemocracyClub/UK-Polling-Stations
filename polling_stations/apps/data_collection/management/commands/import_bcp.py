from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000058"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019BCp.CSV"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019BCp.CSV"
    elections = ["europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "BH3 7JX":
            return None

        if record.addressline6 == "BH23 4FZ":
            rec["postcode"] = "BH234FS"

        if uprn in ["10094069238", "10094069090", "10094069239", "10094069240"]:
            rec["postcode"] = "BH14EH"

        if uprn == "100040574446":
            rec["postcode"] = "BH237HU"

        if record.addressline2 == "4 Windermere Road":
            rec["postcode"] = "BH37LF"

        return rec
