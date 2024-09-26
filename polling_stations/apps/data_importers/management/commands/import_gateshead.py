from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GAT"
    addresses_name = (
        "2024-07-04/2024-06-04T12:47:09.508645/Democracy_Club__04July2024 (20).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-04T12:47:09.508645/Democracy_Club__04July2024 (20).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100000002781",  # RIDING CHASE, NORMANS RIDING POULTRY FARM, BLAYDON-ON-TYNE
                "10024187494",  # UNIT A2 CONTRACT HOUSE WELLINGTON ROAD, DUNSTON, GATESHEAD
                "100000017168",  # 74 BENSHAM ROAD, GATESHEAD
                "100000017167",  # 72 BENSHAM ROAD, GATESHEAD
                "100000017169",  # 76 BENSHAM ROAD, GATESHEAD
                "100000034744",  # 6 HAMBLETON GREEN, GATESHEAD
                "10022984423",  # HIGH EIGHTON FARM HOUSE BLACK LANE, HARLOW GREEN, GATESHEAD
                "10022993225",  # NO WORRYS ST CUTHBERTS MEWS SIDMOUTH ROAD, CHOWDENE, GATESHEAD
                "10093488362",  # 16 BIRCH CRESCENT, BIRTLEY, CHESTER LE STREET
                "10093488193",  # 10 BIRCH CRESCENT, BIRTLEY, CHESTER LE STREET
                "10093487880",  # 5 MAPLE AVENUE, BIRTLEY, CHESTER LE STREET
                "100000074532",  # CHEVVY CHASE, PENNYFINE ROAD, SUNNISIDE, NEWCASTLE UPON TYNE
                "100000074529",  # 130 PENNYFINE ROAD, SUNNISIDE, NEWCASTLE UPON TYNE
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "NE9 5XP",
            "NE9 6JR",
            # looks wrong
            "NE39 2EA",
            "NE10 9HL",
        ]:
            return None

        return super().address_record_to_dict(record)
