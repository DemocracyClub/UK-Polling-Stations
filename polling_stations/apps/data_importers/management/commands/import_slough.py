from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SLG"
    addresses_name = (
        "2023-05-04/2023-04-21T14:19:22.418906/Democracy_Club__04May2023_Slough.CSV"
    )
    stations_name = (
        "2023-05-04/2023-04-21T14:19:22.418906/Democracy_Club__04May2023_Slough.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001911252",  # FLAT 35, PRIORY HEIGHTS, BUCKINGHAM AVENUE, SLOUGH
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SL1 2LT",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Centre, Farnham Road, Slough, SL1 4UT
        # postcode in a wrong column, just moving it to the right place
        if record.polling_place_id == "2305":
            record = record._replace(polling_place_postcode="SL1 4UT")

        return super().station_record_to_dict(record)
