from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STH"
    addresses_name = (
        "2024-07-04/2024-06-09T17:28:00.538366/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-09T17:28:00.538366/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "SO15 2NS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Ascension Centre (Grace Hall), 1 Thorold Road, Southampton, SO18 1HZ
        # The Ascension Centre (Vite Room, 1 Thorold Road, Southampton, SO18 1HZ
        if record.polling_place_id in ["15482", "15486"]:
            record = record._replace(
                polling_place_easting="444086", polling_place_northing="113955"
            )

        # Moorlands Community Centre (Main Hall), Townhill Way, Southampton, SO18 2ER
        if record.polling_place_id == "15495":
            record = record._replace(
                polling_place_easting="445540", polling_place_northing="114282"
            )

        return super().station_record_to_dict(record)
