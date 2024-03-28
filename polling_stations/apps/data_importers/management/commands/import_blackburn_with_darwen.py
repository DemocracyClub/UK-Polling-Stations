from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BBD"
    addresses_name = (
        "2024-05-02/2024-03-07T15:26:25.483784/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-07T15:26:25.483784/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    # Following warning checked and no correction needed:
    # WARNING: Polling station Belthorn Primary School (5798) is in Hyndburn Borough Council (HYN)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100012541481",  # DARR CLOTH HOUSE, 5-7 NEW BANK ROAD, BLACKBURN
            "100010753970",  # 2 PLECKGATE ROAD, BLACKBURN
            "10010321691",  # FLAT, 149 WHALLEY OLD ROAD, BLACKBURN
            "200004508099",  # CARETAKERS FLAT SOMME BARRACKS MOSS STREET, BLACKBURN
            "10010324584",  # STUDENT ACCOMODATION 30 MOSS STREET, BLACKBURN
            "10091620653",  # 197A AUDLEY RANGE, BLACKBURN
            "100010730844",  # 1 ARRAN AVENUE, BLACKBURN
            "10024626659",  # FLAT AT 51 MARKET STREET, DARWEN
            "10010322678",  # 150A BLACKBURN ROAD, DARWEN
            "100010759333",  # 83 SHORROCK LANE, BLACKBURN
            "100010732406",  # 53 BEECHWOOD DRIVE, BLACKBURN
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BB3 2NQ",
            "BB1 7LS",
            "BB1 7LT",
            "BB1 2NL",
            "BB1 1EB",
            # looks wrong
            "BB2 6TE",
            "BB2 2SS",
            "BB1 1JS",
            "BB3 3QP",
            # "BB2 5FT",  # waiting for council response
            # "BB2 5FX",  # waiting for council response
        ]:
            return None

        return super().address_record_to_dict(record)
