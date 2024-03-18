from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRM"
    addresses_name = (
        "2024-05-02/2024-03-18T11:26:35.230552/Bromsgrove Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-18T11:26:35.230552/Bromsgrove Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100120560854",  # 34 GUNNER LANE, RUBERY, REDNAL, BIRMINGHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "B61 0NX",
            "B45 8HY",
            "DY9 9XT",
            "B60 3AZ",
            "B48 7BS",
            "B61 7AY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Warnings below checked and no correction needed:
        # WARNING: Polling station Broadmeadow Junior School (7941) is in Birmingham City Council (BIR)

        # adding point for: Changing Rooms Barnsley Hall, off Barnsley Hall Road, Bromsgrove, B61 0EX
        if record.polling_place_id == "7948":
            record = record._replace(
                polling_place_easting="396005", polling_place_northing="272868"
            )

        # adding point for: Catshill Village Hall, Golden Cross Lane, Catshill, B61 0JZ
        if record.polling_place_id == "8218":
            record = record._replace(
                polling_place_easting="396119", polling_place_northing="274035"
            )

        # adding point for: Cofton Village Hall, Community Centre, 1 Village Hall Way, Cofton Hackett, B45 8PD
        if record.polling_place_id == "8068":
            record = record._replace(
                polling_place_easting="400942", polling_place_northing="276167"
            )

        # adding point for: Beacon Suite at The Old Rose and Crown Hotel, Rose Hill, Lickey, B45 8RT
        if record.polling_place_id == "8217":
            record = record._replace(
                polling_place_easting="399517", polling_place_northing="275838"
            )

        return super().station_record_to_dict(record)
