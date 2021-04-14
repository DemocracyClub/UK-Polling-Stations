from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HCK"
    addresses_name = (
        "2021-04-14T17:18:14.166273/Democracy_club_with_coords_06May2021.csv"
    )
    stations_name = (
        "2021-04-14T17:18:14.166273/Democracy_club_with_coords_06May2021.csv"
    )
    elections = ["2021-05-06"]
    csv_encoding = "utf-8-sig"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008353260",  # BASEMENT FLAT, 75 ICKBURGH ROAD, LONDON
            "10008322617",  # FLAT 2 357A WICK ROAD, HACKNEY, LONDON
            "10008245689",  # SECOND FLOOR FLAT 126 KINGSLAND HIGH STREET, HACKNEY, LONDON
            "10008349782",  # 3 MIAH HOUSE 149D BROOKE ROAD, HACKNEY, LONDON
            "10008342758",  # 1 MIAH HOUSE 149D BROOKE ROAD, HACKNEY, LONDON
            "10008342260",  # 20 MILLFIELDS PARADE, MILLFIELDS ROAD, LONDON
            "100021050062",  # BASEMENT AND GROUND FLOOR 100 LOWER CLAPTON ROAD, HACKNEY, LONDON
            "10008294596",  # 1A SHEPHERDESS WALK, LONDON
            "10008294592",  # FIRST FLOOR AND SECOND FLOOR FLAT 111 STOKE NEWINGTON ROAD, HACKNEY, LONDON
            "10008294594",  # FLAT, 97 STOKE NEWINGTON ROAD, LONDON
            "10008294598",  # 2 MIAH HOUSE 149D BROOKE ROAD, HACKNEY, LONDON
            "10008306167",  # 4 MIAH HOUSE 149D BROOKE ROAD, HACKNEY, LONDON
            "100021076655",  # 10 CORNTHWAITE ROAD, LONDON
            "10008318539",  # FLAT B 45 STOKE NEWINGTON CHURCH STREET, HACKNEY, LONDON
            "10008340028",  # FLAT E, 112 KINGSLAND ROAD, LONDON
            "100021030699",  # 108 GEORGE DOWNING ESTATE, CAZENOVE ROAD, LONDON
            "10008300957",  # 85 CASTLEWOOD ROAD, HACKNEY, LONDON
            "10008245689",  # SECOND FLOOR FLAT 126 KINGSLAND HIGH STREET, HACKNEY, LONDON
            "10008245688",  # FIRST FLOOR FLAT 126 KINGSLAND HIGH STREET, HACKNEY, LONDON
            "10008245690",  # THIRD FLOOR FLAT 126 KINGSLAND HIGH STREET, HACKNEY, LONDON
            "100021051676",  # SECOND FLOOR FLAT 417 KINGSLAND ROAD, HACKNEY, LONDON
            "200001073528",  # POTTERY HOUSE, ELRINGTON ROAD, LONDON
        ]:
            return None

        if record.addressline6 in [
            "E2 8FZ",
            "E5 8BE",
            "N16 0SD",
            "N16 0RT",
            "N4 2WN",
            "N4 2LD",
            "E8 3RL",
        ]:
            return None

        return super().address_record_to_dict(record)
