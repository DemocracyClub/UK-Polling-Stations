from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOL"
    addresses_name = (
        "2026-05-07/2026-04-02T15:14:58.840898/Democracy_Club__07May2026_Bolton.CSV"
    )
    stations_name = (
        "2026-05-07/2026-04-02T15:14:58.840898/Democracy_Club__07May2026_Bolton.CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10070916825",  # CURLEYS FISHERY, TOP O TH WALLSUCHES, HORWICH, BOLTON
                "100012431797",  # 321 DERBY STREET, BOLTON
                "100012556511",  # 152 LONGSIGHT, BOLTON
                "10001244221",  # FLAT 1 290 ST HELENS ROAD, BOLTON
                "10001245228",  # METHODIST CHURCH DICCONSON LANE, ASPULL, BOLTON
                "100012558543",  # PARFEN LIMITED, SUNNYSIDE NURSING HOME ADELAIDE STREET, BOLTON
                "200002544033",  # 2 CUTACRE LANE, BOLTON
                "100012430429",  # ROYAL HOTEL, 142 ALBERT ROAD, FARNWORTH, BOLTON
                "100012430421",  # HOBOKEN HOUSE, AINSWORTH AVENUE, HORWICH, BOLTON
                "100012552065",  # HOLIDAY INN BOLTON, 1 HIGHER BRIDGE STREET, BOLTON
                "100010918636",  # 659 RADCLIFFE ROAD, BOLTON
                "100012434106",  # HILLSIDE FARM, TOTTINGTON ROAD, BOLTON
                "100012432094",  # FOUR WAYS, GREEN LANE, BOLTON
                "200002551724",  # FLAT 1 62 CHORLEY OLD ROAD, BOLTON
                "200002546015",  # 70 CHORLEY OLD ROAD, BOLTON
                "200002546015",  # 70 CHORLEY OLD ROAD, BOLTON
                "200002551713",  # FLAT 1 65 CHORLEY OLD ROAD, BOLTON
                "200002551714",  # FLAT 2 65 CHORLEY OLD ROAD, BOLTON
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "BL6 4ED",
            "BL4 8JA",
            "BL5 2DL",
            "BL3 2DP",
            "BL4 0LW",
            "BL1 5HP",
            "BL1 2HZ",
            "BL2 4JU",
            "BL3 3JY",
            # looks wrong
            "BL5 2DJ",
            "BL3 2QH",
            "BL1 2HE",
        ]:
            return None

        return super().address_record_to_dict(record)
