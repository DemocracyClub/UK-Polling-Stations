from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "GRT"
    addresses_name = "2026-05-07/2026-02-24T12:43:44.220496/Democracy Club - Idox_2026-02-24 12-26.csv"
    stations_name = "2026-05-07/2026-02-24T12:43:44.220496/Democracy Club - Idox_2026-02-24 12-26.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # Station change from council:
        # OLD: St. Mary's Church (Ash Vale), Vale Road, Ash Vale, Aldershot, GU12 5JE
        # NEW: First Blackwater Valley B-P Scout Hut, Carrington Lane, Ash Vale, Guildford, GU12 5PG
        if self.get_station_hash(record) == "2-st-marys-church-ash-vale":
            record = record._replace(
                pollingstationname="First Blackwater Valley B-P Scout Hut",
                pollingstationaddress1="Carrington Lane",
                pollingstationaddress2="Ash Vale",
                pollingstationaddress3="Guildford",
                pollingstationpostcode="GU12 5PG",
                pollingvenueuprn="10007048977",
                pollingvenueeasting="489059",
                pollingvenuenorthing="153820",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100062134282",  # FLAT 1 30 YORK ROAD, GUILDFORD
            "10007066650",  # 2 MERROW LODGE, CLANDON PARK, WEST CLANDON, GUILDFORD
            "10007066649",  # 1 MERROW LODGE, CLANDON PARK, WEST CLANDON, GUILDFORD
        ]:
            return None
        if record.postcode in [
            # split
            "GU10 1BP",
            "GU2 4LS",
            # suspect
            "GU5 9QN",
        ]:
            return None

        # Station change from council:
        # OLD: St. Mary's Church (Ash Vale), Vale Road, Ash Vale, Aldershot, GU12 5JE
        # NEW: First Blackwater Valley B-P Scout Hut, Carrington Lane, Ash Vale, Guildford, GU12 5PG
        if self.get_station_hash(record) == "2-st-marys-church-ash-vale":
            record = record._replace(
                pollingstationname="First Blackwater Valley B-P Scout Hut",
            )

        return super().address_record_to_dict(record)
