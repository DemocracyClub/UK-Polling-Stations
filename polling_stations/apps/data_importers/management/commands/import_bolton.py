from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOL"
    addresses_name = (
        "2023-05-04/2023-04-17T12:47:32.703993/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-04-17T12:47:32.703993/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070916825",  # CURLEYS FISHERY, TOP O TH WALLSUCHES, HORWICH, BOLTON
            "100012431797",  # 321 DERBY STREET, BOLTON
            "10001244960",  # FLAT 3, 115-117 DERBY STREET, BOLTON
            "100012556511",  # 152 LONGSIGHT, BOLTON
            "10001244221",  # FLAT 1 290 ST HELENS ROAD, BOLTON
            "10001241112",  # ROOF TOP BARN, WINGATES LANE, WESTHOUGHTON, BOLTON
            "100012434531",  # RALPH FOLD COTTAGE, WINGATES LANE, WESTHOUGHTON, BOLTON
            "10001245228",  # METHODIST CHURCH DICCONSON LANE, ASPULL, BOLTON
            "10070924657",  # WHITE WILLOW BARN, JACKS LANE, WESTHOUGHTON, BOLTON
            "100012558543",  # PARFEN LIMITED, SUNNYSIDE NURSING HOME ADELAIDE STREET, BOLTON
            "200002544033",  # 2 CUTACRE LANE, BOLTON
            "100012430429",  # ROYAL HOTEL, 142 ALBERT ROAD, FARNWORTH, BOLTON
            "100012433367",  # BURNTHWAITE COTTAGE, OLD HALL LANE, LOSTOCK, BOLTON
            "100012434106",  # HILLSIDE FARM, TOTTINGTON ROAD, BOLTON
            "100010918637",  # 660 RADCLIFFE ROAD, BOLTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BL5 2DL",
            "BL4 8JA",
            "BL1 3SJ",
            "BL6 4ED",
            "BL2 4JU",
            "BL3 2DP",
            "BL4 0LW",
            "BL1 5HP",
            "BL1 2HZ",
            "BL1 7NS",  # HARRICROFT FARM COTTAGES SMITHILLS DEAN ROAD, BOLTON
        ]:
            return None

        rec = super().address_record_to_dict(record)

        # Replace the wrong letter "O" with the correct number "0"
        if record.addressline6.strip() in ["BL7 OHR", "BL4 ONX", "BL4 ONY"]:
            rec["postcode"] = rec["postcode"].replace("O", "0")

        return rec
