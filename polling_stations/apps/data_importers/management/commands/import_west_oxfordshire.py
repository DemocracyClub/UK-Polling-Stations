from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOX"
    addresses_name = (
        "2022-05-05/2022-03-17T09:27:17.244620/Democracy Club Export for 220505.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-17T09:27:17.244620/Democracy Club Export for 220505.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Brize Norton Elder Bank Hall
        if record.polling_place_id == "7807":
            record = record._replace(polling_place_postcode="OX18 3PU")
            record = record._replace(polling_place_easting="430059")
            record = record._replace(polling_place_northing="207340")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in ["OX20 1RZ", "OX18 3HW", "OX18 3NU"]:
            return None  # split

        return super().address_record_to_dict(record)
