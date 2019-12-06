from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000102"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "latin-1"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10090789736":
            rec["postcode"] = "WD5 0GF"

        if uprn in [
            "100081289658",  # WD35LW -> WD35LL : Viewpoint, Old Common Road, Chorleywood, Rickmansworth, Hertfordshire
            "200000943009",  # WD35NL -> WD33AN : 3A New Parade, Chorleywood, Rickmansworth, Hertfordshire
        ]:
            rec["accept_suggestion"] = False

        return rec
