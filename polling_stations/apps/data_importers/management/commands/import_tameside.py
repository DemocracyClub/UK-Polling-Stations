from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAM"
    addresses_name = (
        "2024-07-04/2024-06-05T16:20:34.774781/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-05T16:20:34.774781/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090073761",  # 19A WELLINGTON STREET, ASHTON-UNDER-LYNE
            "10090073763",  # 21A WELLINGTON STREET, ASHTON-UNDER-LYNE
            "10090073764",  # 21B WELLINGTON STREET, ASHTON-UNDER-LYNE
            "200004419358",  # FLAT 2 34 HUDSON ROAD, HYDE
            "10096633108",  # 1 TAYLOR STREET, DENTON, MANCHESTER
            "10096633109",  # 3 TAYLOR STREET, DENTON, MANCHESTER
            "200004410061",  # FLAT 2 2 OLD HALL LANE, MOTTRAM
            "100012777909",  # HOPKINS FARM COTTAGE, ARLIES LANE, STALYBRIDGE
            "100012777908",  # HOPKINS COTTAGE, ARLIES LANE, STALYBRIDGE
            "100011600288",  # 39 MARKET STREET, DENTON, MANCHESTER
            "100011545502",  # 2 JOHN STREET, DENTON, MANCHESTER
            "10014255906",  # THE HOLLIES BUNGALOW, BOYDS WALK, DUKINFIELD
            "200002857633",  # PORTLAND BASIN MARINA, LOWER ALMA STREET, DUKINFIELD
            "10014258331",  # ARMSTRONGS OFFICE FURNITURE, 29 PENNY MEADOW, ASHTON-UNDER-LYNE
        ]:
            return None

        if record.addressline6 in [
            # split
            "OL6 9LS",
            "M34 7RZ",
            "M43 6NY",
            "SK15 3QZ",
            "M43 7ZD",
            # suspect
            "SK14 4RD",
        ]:
            return None
        return super().address_record_to_dict(record)
