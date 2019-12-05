from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000220"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10010524278":
            rec["postcode"] = "CV7 9LX"

        if uprn in [
            "100070189342"  # CV227JT -> CV227JS : 83 Lawford Lane, Bilton, Rugby
        ]:
            rec["accept_suggestion"] = False

        if record.addressline6.strip() in ["CV21 1SB", "CV23 9DU", "CV23 9BG"]:
            return None

        return rec
