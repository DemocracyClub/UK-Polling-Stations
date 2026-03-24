from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BBD"
    addresses_name = (
        "2026-05-07/2026-03-24T11:41:56.121266/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-24T11:41:56.121266/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    # Following warning checked and no correction needed:
    # WARNING: Polling station Belthorn Primary School (6760) is in Hyndburn Borough Council (HYN)

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
            "10096074998",  # FLAT AT 82-84 BOLTON ROAD, BLACKBURN
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BB1 7LS",
            "BB1 2NL",
            "BB3 2NQ",
            # looks wrong
            "BB2 6TE",
            "BB2 2SS",
            "BB1 1JS",
            "BB3 3QP",
        ]:
            return None

        return super().address_record_to_dict(record)
