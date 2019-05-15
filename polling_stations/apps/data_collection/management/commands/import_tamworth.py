from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000199"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Tamworth.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Tamworth.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        # Uprn and address match to abp, but council postcode probably incorrect.
        if record.property_urn.strip().lstrip("0") == "394034102":
            rec["postcode"] = "B78 3XD"

        return rec
