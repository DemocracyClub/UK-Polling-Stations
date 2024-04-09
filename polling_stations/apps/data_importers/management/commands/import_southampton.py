from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STH"
    addresses_name = (
        "2024-05-02/2024-04-09T19:58:39.347148/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-09T19:58:39.347148/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "SO16 7GQ",
            "SO15 2NS",
            "SO16 7AS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Ascension Centre (Grace Hall), 1 Thorold Road, Southampton, SO18 1HZ
        # The Ascension Centre (Vite Room, 1 Thorold Road, Southampton, SO18 1HZ
        if record.polling_place_id in ["14759", "14756"]:
            record = record._replace(
                polling_place_easting="444086", polling_place_northing="113955"
            )

        # Moorlands Community Centre (Main Hall), Townhill Way, Southampton, SO18 2ER
        if record.polling_place_id == "14808":
            record = record._replace(
                polling_place_easting="445540", polling_place_northing="114282"
            )

        return super().station_record_to_dict(record)
