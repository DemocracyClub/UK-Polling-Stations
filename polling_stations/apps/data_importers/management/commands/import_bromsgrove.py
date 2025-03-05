from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRM"
    addresses_name = (
        "2025-05-01/2025-03-05T12:03:17.688205/Democracy_Club__01May2025 Bromsgrove.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-05T12:03:17.688205/Democracy_Club__01May2025 Bromsgrove.CSV"
    )
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "B48 7BS",
            "B61 0NX",
            "B60 3AZ",
            "B45 8HY",
            "B61 7AY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Warnings below checked and no correction needed:
        # WARNING: Polling station Broadmeadow Junior School (8390) is in Birmingham City Council (BIR)

        # adding point for: Catshill Village Hall, Golden Cross Lane, Catshill, B61 0JZ
        if record.polling_place_id == "8985":
            record = record._replace(
                polling_place_easting="396119", polling_place_northing="274035"
            )

        # adding point for: Beacon Suite at The Old Rose and Crown Hotel, Rose Hill, Lickey, B45 8RT
        if record.polling_place_id == "8989":
            record = record._replace(
                polling_place_easting="399517", polling_place_northing="275838"
            )

        return super().station_record_to_dict(record)
