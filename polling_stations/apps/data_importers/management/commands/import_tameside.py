from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAM"
    addresses_name = (
        "2026-05-07/2026-04-15T15:19:09.350583/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-04-15T15:19:09.350583/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100011577205",  # THE BUTTY BOX, 86 MOTTRAM ROAD, HYDE
                "10096633534",  # 2 BENTINCK STREET, ASHTON-UNDER-LYNE, OL7 0PT
                "10096634016",  # 10 SANDY BANK AVENUE, HYDE, SK14 3GN
                "200004402872",  # 148 MOSSLEY ROAD, ASHTON-UNDER-LYNE, OL6 6NA
                "10093147227",  # NARROWBOAT LUCKATY PORTLAND BASIN MARINA LOWER ALMA STREET, DUKINFIELD, SK16 4SQ
                "100012741804",  # 4 MANCHESTER ROAD, ASHTON-UNDER-LYNE, OL7 0BA
                "10096636877",  # FLAT ABOVE 457 EDGE LANE, DROYLSDEN, M43 6JN
                "10096635427",  # APARTMENT 3, FABRIC HOUSE, HOWARDS COURT, ASHTON-UNDER-LYNE, OL6 6AW
                "10093146981",  # 39 WARBLIN WAY, STALYBRIDGE, SK15 1FG
                "10096633108",  # 1 TAYLOR STREET, DENTON, MANCHESTER
                "10096633109",  # 3 TAYLOR STREET, DENTON, MANCHESTER
                "100012488220",  # 105 THORNLEY LANE SOUTH, STOCKPORT
                "10090073761",  # 19A WELLINGTON STREET, ASHTON-UNDER-LYNE
                "10090073763",  # 21A WELLINGTON STREET, ASHTON-UNDER-LYNE
                "10090073764",  # 21B WELLINGTON STREET, ASHTON-UNDER-LYNE
                "200004419358",  # FLAT 2 34 HUDSON ROAD, HYDE
                "200004410061",  # FLAT 2 2 OLD HALL LANE, MOTTRAM
                "100012777909",  # HOPKINS FARM COTTAGE, ARLIES LANE, STALYBRIDGE
                "100012777908",  # HOPKINS COTTAGE, ARLIES LANE, STALYBRIDGE
                "100011545502",  # 2 JOHN STREET, DENTON, MANCHESTER
                "10014255906",  # THE HOLLIES BUNGALOW, BOYDS WALK, DUKINFIELD
                "200002857633",  # PORTLAND BASIN MARINA, LOWER ALMA STREET, DUKINFIELD
                "10014258331",  # ARMSTRONGS OFFICE FURNITURE, 29 PENNY MEADOW, ASHTON-UNDER-LYNE
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "SK15 2LU",
            "OL6 9LS",
            "SK15 3QZ",
            "M34 7RZ",
            "M43 7BF",
            "M43 7ZD",
            # suspect
            "SK14 4RD",
            "M43 7PU",
            "SK14 5AR",
            "OL6 6AW",
            "OL6 8AS",
        ]:
            return None
        return super().address_record_to_dict(record)
