from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000229"
    addresses_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018WORTHresp.tsv"
    stations_name = "local.2018-05-03/Version 2/Democracy_Club__03May2018WORTHresp.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["100061896711", "100061896712"]:
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "BN13 3PB"
            return rec

        return super().address_record_to_dict(record)
