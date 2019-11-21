from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000091"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019nf.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019nf.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["10007461147", "100062214501"]:
            return None

        return rec
