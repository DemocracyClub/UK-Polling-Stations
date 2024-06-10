from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SLG"
    addresses_name = (
        "2024-07-04/2024-06-10T11:04:14.131183/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-10T11:04:14.131183/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "SL1 2LT",
            "SL1 1LU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Centre, Farnham Road, Slough, SL1 4UT
        # postcode in a wrong column, just moving it to the right place
        if record.polling_place_id == "2736":
            record = record._replace(polling_place_postcode="SL1 4UT")

        return super().station_record_to_dict(record)
