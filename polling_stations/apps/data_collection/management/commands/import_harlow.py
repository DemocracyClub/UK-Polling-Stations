from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000073"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019harlow.CSV"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019harlow.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in ["CM17 0GE", "CM17 9DS"]:
            return None
        if uprn in ["10023423798", "100091437906"]:
            return None

        if uprn in [
            "200002566340"  # CM179LU -> CM179DS : The Farmhouse, London Road, Harlow, Essex
        ]:
            rec["accept_suggestion"] = False

        return rec
