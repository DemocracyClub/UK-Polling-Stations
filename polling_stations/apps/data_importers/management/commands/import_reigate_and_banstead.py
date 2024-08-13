from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "REI"
    addresses_name = (
        "2024-07-04/2024-06-05T14:13:19.010990/REI_Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-05T14:13:19.010990/REI_Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.lstrip("0")

        if (
            uprn
            in [
                "68134095",  # CHIDWELL FARMING, NICOLA FARM, 37 WWOODMANSTERNE LANE, BANSTEAD
                "68137043",  # 170 DOVERS GREEN ROAD, REIGATE
                "68137147",  # 168 DOVERS GREEN ROAD, REIGATE
                "68183366",  # MYRTLE COTTAGE, HORLEY LODGE LANE, REDHILL
                "68115368",  # 1 DEAN LANE, MERSTHAM, REDHILL
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "RH6 8DU",
        ]:
            return None

        return super().address_record_to_dict(record)
