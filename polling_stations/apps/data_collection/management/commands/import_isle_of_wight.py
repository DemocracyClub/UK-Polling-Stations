from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000046"
    addresses_name = "parl.2019-12-12/Version 1/iow.gov.uk-1573036635000-.tsv"
    stations_name = "parl.2019-12-12/Version 1/iow.gov.uk-1573036635000-.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        if record.addressline1 == "Le Sage":
            rec["postcode"] = "PO390AD"

        if record.addressline1 == "Rookley Holiday Park":
            rec["postcode"] = "PO383LU"
        if (
            record.addressline1 == "Flat 15 Solent House"
            and record.addressline6 == "PO30 5TG"
        ):
            return None

        if record.addressline1 == "Down House":
            return None

        return rec
