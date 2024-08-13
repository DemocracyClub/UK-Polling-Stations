from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DOV"
    addresses_name = "2024-07-04/2024-05-30T10:38:09.548818/DoverDC Democracy_Club__04July2024 (1).CSV"
    stations_name = "2024-07-04/2024-05-30T10:38:09.548818/DoverDC Democracy_Club__04July2024 (1).CSV"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10034885006",  # MANAGERS ACCOMMODATION 9 CASTLE HILL ROAD, DOVER
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
                "100060883820",  # CRIXHALL HOUSE, BUCKLAND LANE, STAPLE, CANTERBURY
                "10034882943",  # THE WILLOWS, SANDWICH ROAD, HACKLINGE, DEAL
                "10034875431",  # ADELAIDE FARM HOUSE, SANDWICH ROAD, HACKLINGE, DEAL
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
