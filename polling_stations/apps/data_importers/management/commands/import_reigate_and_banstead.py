from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "REI"
    addresses_name = (
        "2025-05-01/2025-03-26T10:26:14.227748/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-26T10:26:14.227748/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    # By-election script so maintaing previous exclusions as comments for future reference
    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.lstrip("0")

    #     if (
    #         uprn
    #         in [
    #             "68134095",  # CHIDWELL FARMING, NICOLA FARM, 37 WWOODMANSTERNE LANE, BANSTEAD
    #             "68137043",  # 170 DOVERS GREEN ROAD, REIGATE
    #             "68137147",  # 168 DOVERS GREEN ROAD, REIGATE
    #             "68183366",  # MYRTLE COTTAGE, HORLEY LODGE LANE, REDHILL
    #             "68115368",  # 1 DEAN LANE, MERSTHAM, REDHILL
    #         ]
    #     ):
    #         return None

    #     if record.addressline6 in [
    #         # splits
    #         "RH6 8DU",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)
