from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRM"
    addresses_name = (
        "2026-11-26/2026-10-22T10:39:51.879075/Democracy_Club__26November2026.tsv"
    )
    stations_name = (
        "2026-11-26/2026-10-22T10:39:51.879075/Democracy_Club__26November2026.tsv"
    )
    elections = ["2026-11-26"]
    csv_delimiter = "\t"

    # maintaining tweaks as comments through by-election

    # def address_record_to_dict(self, record):
    #     if record.addressline6 in [
    #         # splits
    #         "B48 7BS",
    #         "B61 0NX",
    #         "B60 3AZ",
    #         "B45 8HY",
    #         "B61 7AY",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)

    # def station_record_to_dict(self, record):
    #     # Warnings below checked and no correction needed:
    #     # WARNING: Polling station Broadmeadow Junior School (8390) is in Birmingham City Council (BIR)

    #     # adding point for: Catshill Village Hall, Golden Cross Lane, Catshill, B61 0JZ
    #     if record.polling_place_id == "8985":
    #         record = record._replace(
    #             polling_place_easting="396119", polling_place_northing="274035"
    #         )

    #     # adding point for: Beacon Suite at The Old Rose and Crown Hotel, Rose Hill, Lickey, B45 8RT
    #     if record.polling_place_id == "8989":
    #         record = record._replace(
    #             polling_place_easting="399517", polling_place_northing="275838"
    #         )

    #     return super().station_record_to_dict(record)
