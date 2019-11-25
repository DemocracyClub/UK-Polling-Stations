from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):

    council_id = "W06000015"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019cardiff.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019cardiff.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10023549342":
            rec["postcode"] = "CF240ES"
        if uprn == "200001679322":
            rec["postcode"] = "CF118HP"
        if record.addressline6 in ["CF72 8NS", "CF14 9UA"]:
            return None

        if uprn in ["200001679752", "10002509644"]:
            return None

        return rec
