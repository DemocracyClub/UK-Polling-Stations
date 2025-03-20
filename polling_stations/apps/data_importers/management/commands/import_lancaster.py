from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LAC"
    addresses_name = (
        "2025-05-01/2025-03-20T10:13:08.250557/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-20T10:13:08.250557/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10009269943",  # LING COTTAGE, CRAG FOOT, WARTON, CARNFORTH
                "10091522599",  # 53 TWIN LAKES COUNTRY CLUB BURTON ROAD, TEWITFIELD
                "10009274881",  # LECK FELL HOUSE, LECK, CARNFORTH
                "10009274155",  # PARK HOUSE FARM, TATHAM, LANCASTER
                "200000657611",  # HOLEHOUSE FARM, CATON GREEN ROAD, CATON GREEN, LANCASTER
                "100012622526",  # WHITE CROSS PUB, QUARRY ROAD, LANCASTER
                "100012394574",  # WOODSIDE, BOWERHAM ROAD, LANCASTER
                "100012394393",  # WILSON HOUSE, ASHTON ROAD, LANCASTER
                "100012622911",  # LANCASTER HOUSE HOTEL, GREEN LANE, ELLEL, LANCASTER
                "10009280294",  # BLACK HOUSE FARM, ELLEL, LANCASTER
                "10009278691",  # THORNCLIFFE, ELLEL, LANCASTER
                "100012396351",  # BANK HOUSE FARM, THURNHAM, LANCASTER
                "100012622683",  # 120 BOWERHAM ROAD, LANCASTER
                "10009274369",  # HALF MOON HOUSE, BARROWS LANE, HEYSHAM, MORECAMBE
                "100010479648",  # 115 ALEXANDRA ROAD, MORECAMBE
                "100012624238",  # 2 BRUNSWICK ROAD, HEYSHAM, MORECAMBE
                "100010494859",  # 53 SCHOLA GREEN LANE, MORECAMBE
                "100010489113",  # 251 LANCASTER ROAD, MORECAMBE
                "10024269650",  # FLAT BABAR ELEPHANT MORECAMBE ROAD, LANCASTER
                "100010476805",  # 179 TORRISHOLME ROAD, LANCASTER
                "100010460511",  # 60 BARLEY COP LANE, LANCASTER
                "100010460513",  # 62 BARLEY COP LANE, LANCASTER
                "100012622109",  # ST, JOSEPHS PRESBYTERY, SLYNE ROAD, LANCASTER
                "10009274651",  # THE COTTAGE, NEW HOUSE FARM, LANCASTER ROAD, SLYNE, LANCASTER
                "10009280758",  # HAERE MAI, SLYNE, LANCASTER
                "10009273926",  # HAMMERTON HALL, SLYNE, LANCASTER
                "200001700610",  # THREE MILE COTTAGE, CROOK O LUNE, LANCASTER
                "200001700611",  # THREE MILE HOUSE, CROOK O LUNE, LANCASTER
                "200000657611",  # HOLEHOUSE FARM, CATON GREEN ROAD, CATON GREEN, LANCASTER
                "200000657610",  # CROFTLANDS, CATON GREEN ROAD, CATON GREEN, LANCASTER
                "10009283592",  # THE BARN, ADDINGTON ROAD, HALTON, LANCASTER
                "100012395239",  # OATLANDS FARM, GRAB LANE, LANCASTER
                "100012395247",  # SOUTH LODGE, GREAVES ROAD, LANCASTER
                "10009268690",  # 2 RIPLEY STREET, LANCASTER
                "100012394409",  # FLAT 5 ASHTON COURT ASHTON ROAD, LANCASTER
                "100012394410",  # FLAT 6 ASHTON COURT ASHTON ROAD, LANCASTER
                "100010476800",  # 170 TORRISHOLME ROAD, LANCASTER
                "100010476801",  # 172 TORRISHOLME ROAD, LANCASTER
                "100010477611",  # 1 WATERY LANE, LANCASTER
                "200001648068",  # BOAT HOUSE LOW ROAD, HALTON
                "100010490148",  # 2 LOW LANE, MORECAMBE
                "10009284148",  # PRINGLES COTTAGE, CARNFORTH
                "100010456069",  # 154 LANCASTER ROAD, CARNFORTH
                "10009273098",  # COACH HOUSE, BURROW HEIGHTS LANE, LANCASTER
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "LA1 3TE",
            "LA1 3LY",
            "LA1 1AF",
            "LA2 6AL",
            "LA2 6AS",
            "LA2 0AQ",
            "LA5 0SW",
            # suspect
            "LA1 3JJ",
            "LA1 5AH",
            "LA3 3DD",
            "LA4 6RU",
            "LA2 8NN",
        ]:
            return None

        return super().address_record_to_dict(record)
