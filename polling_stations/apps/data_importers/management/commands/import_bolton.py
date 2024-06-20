from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOL"
    addresses_name = (
        "2024-07-04/2024-06-20T16:20:19.994021/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-20T16:20:19.994021/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070916825",  # CURLEYS FISHERY, TOP O TH WALLSUCHES, HORWICH, BOLTON
            "100012431797",  # 321 DERBY STREET, BOLTON
            "100012556511",  # 152 LONGSIGHT, BOLTON
            "10001244221",  # FLAT 1 290 ST HELENS ROAD, BOLTON
            "10001241112",  # ROOF TOP BARN, WINGATES LANE, WESTHOUGHTON, BOLTON
            "100012434531",  # RALPH FOLD COTTAGE, WINGATES LANE, WESTHOUGHTON, BOLTON
            "10001245228",  # METHODIST CHURCH DICCONSON LANE, ASPULL, BOLTON
            "100012558543",  # PARFEN LIMITED, SUNNYSIDE NURSING HOME ADELAIDE STREET, BOLTON
            "200002544033",  # 2 CUTACRE LANE, BOLTON
            "100012430429",  # ROYAL HOTEL, 142 ALBERT ROAD, FARNWORTH, BOLTON
            "100012430421",  # HOBOKEN HOUSE, AINSWORTH AVENUE, HORWICH, BOLTON
            "100012552065",  # HOLIDAY INN BOLTON, 1 HIGHER BRIDGE STREET, BOLTON
            "100010918636",  # 659 RADCLIFFE ROAD, BOLTON
            "100012434106",  # HILLSIDE FARM, TOTTINGTON ROAD, BOLTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BL1 2HZ",
            "BL1 2JU",
            "BL1 5HP",
            "BL2 4JU",
            "BL3 2DP",
            "BL3 3GR",
            "BL3 3JY",
            "BL4 0LW",
            "BL4 8JA",
            "BL5 2DL",
            "BL6 4ED",
            # looks wrong
            "BL5 2DJ",
            "BL3 2QH",
            "BL1 2HE",
            "BL3 3GR",
        ]:
            return None

        return super().address_record_to_dict(record)
