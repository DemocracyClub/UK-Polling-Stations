from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRM"
    addresses_name = "2024-07-04/2024-06-06T10:34:34.598327/Bromsgrove Democracy_Club__04July2024.CSV"
    stations_name = "2024-07-04/2024-06-06T10:34:34.598327/Bromsgrove Democracy_Club__04July2024.CSV"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100120560854",  # 34 GUNNER LANE, RUBERY, REDNAL, BIRMINGHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "B60 3AZ",
            "B61 0NX",
            "B48 7BS",
            "B45 8HY",
            "DY9 9XT",
            "B61 7AY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Warnings below checked and no correction needed:
        # WARNING: Polling station Broadmeadow Junior School (8390) is in Birmingham City Council (BIR)

        # adding point for: Catshill Village Hall, Golden Cross Lane, Catshill, B61 0JZ
        if record.polling_place_id == "8401":
            record = record._replace(
                polling_place_easting="396119", polling_place_northing="274035"
            )

        # adding point for: Beacon Suite at The Old Rose and Crown Hotel, Rose Hill, Lickey, B45 8RT
        if record.polling_place_id == "8405":
            record = record._replace(
                polling_place_easting="399517", polling_place_northing="275838"
            )

        return super().station_record_to_dict(record)
