from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DOV"
    addresses_name = (
        "2025-05-01/2025-03-12T15:56:09.094358/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-12T15:56:09.094358/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10034877732",  # MOUNT PLEASANT, DENTON LANE, WOOTTON, CANTERBURY
                "10094398745",  # 3 OAK TREE FARM, ALKHAM, DOVER
                "10094398744",  # 2 OAK TREE FARM, ALKHAM, DOVER
                "10094398743",  # 1 OAK TREE FARM, ALKHAM, DOVER
                "10034877135",  # COPT HILL FARM, WEST HOUGHAM, DOVER
                "10034875463",  # FERN FARM, ABBEY ROAD, HOUGHAM, DOVER
                "10034889700",  # MANAGERS ACCOMMODATION THE PLOUGH INN BEEFEATER FOLKESTONE ROAD, CHURCH HOUGHAM
                "100060911692",  # 53 PRIORY HILL, DOVER
                "100060911690",  # 51 PRIORY HILL, DOVER
                "10034873939",  # UPDOWN LODGE, UPDOWN, BETTESHANGER, DEAL
                "10034875431",  # ADELAIDE FARM HOUSE, SANDWICH ROAD, HACKLINGE, DEAL
                "10096171213",  # THE BARGE J W, RICHBOROUGH ROAD, RICHBOROUGH, SANDWICH
                "10096168842",  # COSS, RICHBOROUGH ROAD, RICHBOROUGH, SANDWICH
                "100062059067",  # FIRST FLOOR AND SECOND FLOOR FLAT 13 KING STREET, DEAL
            ]
        ):
            return None

        if record.addressline6 in [
            # suspect
            "CT3 2BW",
            "CT14 7PA",
            "CT14 6AE",
        ]:
            return None

        return super().address_record_to_dict(record)
