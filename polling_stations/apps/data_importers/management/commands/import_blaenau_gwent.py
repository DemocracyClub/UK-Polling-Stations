from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "BGW"
    addresses_name = "2026-05-07/2026-03-04T15:13:15.154437/Democracy Club - Idox_2026-03-04 15-11.csv"
    stations_name = "2026-05-07/2026-03-04T15:13:15.154437/Democracy Club - Idox_2026-03-04 15-11.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # The council have confirmed the following stations postcodes as correct:

        # CAERSALEM CHAPEL, PARK VIEW, WAUNLLWYD, EBBW VALE, NP23 6UD
        # CWM COMMUNITY EDUCATION & YOUTH CENTRE, CANNING STREET, CWM, EBBW VALE, NP23 7RD
        # HILLTOP LOG CABIN, DARBY CRESCENT, HILLTOP, EBBW VALE, NP23 6QE
        # HOLY TRINITY & ST ANNES CHURCH, CHURCH PLACE, KING STREET, NANTYGLO, NP23 4LB
        # ORPHEUS MUSIC CENTRE, RAWLINSON TERRACE, TREDEGAR, NP22 4LF
        # THE HALL, TIRZAH BAPTIST CHURCH, STATION TERRACE, CWM, EBBW VALE, NP23 6SD
        # TREFIL VILLAGE HALL, TREFIL, TREDEGAR, NP22 4HG
        # WILLIAM POWELL MEMORIAL HALL, BOURNVILLE ROAD, BLAINA, NP13 3ES

        # station change from council:
        # OLD: SIX BELLS BOWLS CLUB, LLWYNON ROAD, SIX BELLS, ABERTILLERY, NP13 2QA
        # NEW: Sixbells Tennis Club, Windsor Road, Sixbells, Abertillery, NP13 2PB
        if self.get_station_hash(record) == "20-six-bells-bowls-club":
            record = record._replace(
                pollingstationname="SIX BELLS TENNIS CLUB",
                pollingstationaddress1="WINDSOR ROAD",
                pollingstationpostcode="NP13 2PB",
                pollingvenueuprn="0",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10014116610",  # 1 MOUNTAIN AIR, EBBW VALE
            "100101035264",  # HILL RISE, LLANGYNIDR ROAD, BEAUFORT, EBBW VALE
        ]:
            return None

        if record.postcode in [
            "NP23 5DH",  # split
        ]:
            return None

        # station change from council:
        if self.get_station_hash(record) == "20-six-bells-bowls-club":
            record = record._replace(
                pollingstationname="SIX BELLS TENNIS CLUB",
            )

        return super().address_record_to_dict(record)
