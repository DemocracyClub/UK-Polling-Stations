from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STH"
    addresses_name = (
        "2023-05-04/2023-04-13T17:56:48.873726/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-13T17:56:48.873726/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "SO15 2NS",
            "SO16 7AS",
            "SO16 7GQ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Royal British Legion Club (Function Room), Windover Close, Southampton, S019 5JS
        # Postcode mistype, should be a letter "O" instead of a number "0"
        if record.polling_place_id == "14024":
            record = record._replace(polling_place_postcode="SO19 5JS")

        # Highfield Church Centre (Lounge), Highfield Lane, Southampton, SO17 7RL
        if record.polling_place_id == "14162":
            record = record._replace(polling_place_postcode="SO17 1RL")

        # Testlands Hub (Spin/Conference Room), (Formerly Millbrook Secondary School), Green Lane, SO16 9RG
        if record.polling_place_id == "14187":
            record = record._replace(polling_place_postcode="SO16 9FQ")

        # The Ascension Centre (Grace Hall), 1 Thorold Road, Southampton, SO18 1HZ
        # The Ascension Centre (Vite Room, 1 Thorold Road, Southampton, SO18 1HZ
        if record.polling_place_id in ["14059", "14056"]:
            record = record._replace(
                polling_place_easting="444086", polling_place_northing="113955"
            )

        # Moorlands Community Centre (Main Hall), Townhill Way, Southampton, SO18 2ER
        if record.polling_place_id == "14106":
            record = record._replace(
                polling_place_easting="445540", polling_place_northing="114282"
            )

        return super().station_record_to_dict(record)
