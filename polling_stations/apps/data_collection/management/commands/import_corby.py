from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000150"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019corby.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019corby.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10024042273":
            rec["postcode"] = "NN17 5EE"

        if record.addressline6 == "NN17 1FP":
            return None

        return rec
