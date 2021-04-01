from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAM"
    addresses_name = "2021-03-19T15:38:04.940947/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-19T15:38:04.940947/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10003436095",  # ASH TREE FARM, HOBSON MOOR ROAD, MOTTRAM, HYDE
            "200004419358",  # FLAT 2 34 HUDSON ROAD, HYDE
            "10090077959",  # FLAT 3, 14 VICTORIA STREET, DENTON, MANCHESTER
            "10090077958",  # FLAT 2, 14 VICTORIA STREET, DENTON, MANCHESTER
            "10090077957",  # FLAT 1, 14 VICTORIA STREET, DENTON, MANCHESTER
            "10090078212",  # COTTAGE REAR OF 49 FAIRFIELD SQUARE, DROYLSDEN
            "100011591969",  # 39 FAIRFIELD SQUARE, DROYLSDEN, MANCHESTER
            "100011584362",  # 1 ARRAS GROVE, DENTON, MANCHESTER
            "100011584364",  # 3 ARRAS GROVE, DENTON, MANCHESTER
            "100011584363",  # 2 ARRAS GROVE, DENTON, MANCHESTER
            "100011584365",  # 4 ARRAS GROVE, DENTON, MANCHESTER
            "10003439283",  # INDIAN PLAZA, 90 AUDENSHAW ROAD, AUDENSHAW, MANCHESTER
            "100012484582",  # THE BOUNDARY, 2 AUDENSHAW ROAD, AUDENSHAW, MANCHESTER
            "100012488602",  # THE VALLEY VIEW, HUDDERSFIELD ROAD, MILLBROOK, STALYBRIDGE
            "200004406539",  # FLAT 2 BANK MILL MANCHESTER ROAD, MOSSLEY
            "10090073761",  # 19A WELLINGTON STREET, ASHTON-UNDER-LYNE
            "10090073763",  # 21A WELLINGTON STREET, ASHTON-UNDER-LYNE
            "10090073764",  # 21B WELLINGTON STREET, ASHTON-UNDER-LYNE
            "200002857633",  # PORTLAND BASIN MARINA, LOWER ALMA STREET, DUKINFIELD
            "10093148018",  # 5 MEADOW VIEW GARDENS, DROYLSDEN
            "10090075504",  # 5 EDMUND STREET, DROYLSDEN
            "10090075502",  # 2 EDMUND STREET, DROYLSDEN, MANCHESTER
            "10090075503",  # 4 EDMUND STREET, DROYLSDEN, MANCHESTER
            "200004409037",  # FLAT 4 62 STAMFORD STREET EAST, ASHTON-UNDER-LYNE
            "200004419592",  # FLAT 6 62 STAMFORD STREET EAST, ASHTON-UNDER-LYNE
            "10014258699",  # 193 MOSSLEY ROAD, ASHTON-UNDER-LYNE
            "10014258700",  # 195 MOSSLEY ROAD, ASHTON-UNDER-LYNE
            "100012777167",  # 36 LORD STREET, STALYBRIDGE
            "100011576995",  # 3 MOTTRAM MOOR, HOLLINGWORTH, HYDE
            "10003441482",  # 78A STOCKPORT ROAD, ASHTON-UNDER-LYNE
            "10014255906",  # THE HOLLIES BUNGALOW, BOYDS WALK, DUKINFIELD
        ]:
            return None

        if record.addressline6 in [
            "OL6 9LS",
            "M43 7ZD",
            "M34 7RZ",
            "SK14 3EB",
            "M34 5US",
            "OL6 7FU",
            "OL7 9NZ",
            "M34 5SH",
            "OL5 9PN",
        ]:
            return None

        return super().address_record_to_dict(record)
