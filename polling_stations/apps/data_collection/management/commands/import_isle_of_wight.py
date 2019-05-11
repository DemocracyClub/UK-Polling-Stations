from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000046"
    addresses_name = "europarl.2019-05-23/Version 1/iow.gov.uk-1556295628000-.tsv"
    stations_name = "europarl.2019-05-23/Version 1/iow.gov.uk-1556295628000-.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        if record.addressline1 == "Le Sage":
            rec["postcode"] = "PO390AD"
        if record.addressline1 == "17 Paddock Road":
            rec["postcode"] = "PO376NZ"
        if record.addressline1 == "Rookley Holiday Park":
            rec["postcode"] = "PO383LU"
        if (
            record.addressline1 == "Flat 15 Solent House"
            and record.addressline6 == "PO30 5TG"
        ):
            return None

        return rec
