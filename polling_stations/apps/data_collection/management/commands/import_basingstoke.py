from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000084"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019basing.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019basing.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn in ["100062463351"]:
            rec["accept_suggestion"] = True

        return rec
