from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000234"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019- Bromsgrove.CSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019- Bromsgrove.CSV"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["100120569259", "10090741909"]:
            return None

        return rec
