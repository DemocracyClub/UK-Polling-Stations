from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAT"
    addresses_name = (
        "2025-05-01/2025-03-26T11:04:35.914526/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-26T11:04:35.914526/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    # By-election script so Maintaining previous exclusions as comments for future reference:
    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")

    #     if uprn in [
    #         "200000999587",  # HOOK CROSS COTTAGE READING ROAD, ROTHERWICK, HOOK
    #         "100060417933",  # STILLERS FARM, EWSHOT LANE, EWSHOT, FARNHAM
    #         "200001011509",  # WILLOW HOUSE, ALBANY ROAD, FLEET
    #         "10008963593",  # 1 OAKTREE PADDOCK, POTBRIDGE, ODIHAM, HOOK
    #         "10008963594",  # 2 OAKTREE PADDOCK POTBRIDGE ROAD, ODIHAM, HOOK
    #         "10008962564",  # BAILEYS FARMHOUSE, ODIHAM ROAD, ODIHAM, HOOK
    #     ]:
    #         return None

    #     if record.addressline6 in [
    #         # split
    #         "RG27 9RJ",
    #         "GU52 0AF",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)

    # def station_record_to_dict(self, record):
    #     # coords from council:
    #     # Yateley Industries, Mill Lane, Yateley, GU46 7TF
    #     if record.polling_place_id == "4703":
    #         record = record._replace(
    #             polling_place_easting="481895",
    #             polling_place_northing="161045",
    #         )
    #     return super().station_record_to_dict(record)
