from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "HER"
    addresses_name = "2024-05-02/2024-03-01T17:12:19.134525/Eros_SQL_Output005.csv"
    stations_name = "2024-05-02/2024-03-01T17:12:19.134525/Eros_SQL_Output005.csv"
    elections = ["2024-05-02"]

    # Following warnings checked and no need for correction:
    # WARNING: Polling station MERIDEN COMMUNITY CENTRE (18-meriden-community-centre) is in Watford Borough Council (WAT)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10013913353",  # THE COTTAGE, CHASE FARM, STAGG HILL, POTTERS BAR
            "10013029889",  # M & T SHEET METAL LTD, KITTS END FARM, KITTS END ROAD, BARNET
            "10013031843",  # SOUTH LODGE, BLACKHORSE LANE, SOUTH MIMMS, POTTERS BAR
            "10034171504",  # SHENLEY LODGE COTTAGE MANOR LODGE SCHOOL RIDGE HILL, SHENLEY
            "10034168386",  # HERTFORDSHIRE PARTNERSHIP NHS TRUST, THE MEADOWS CASTLEFORD CLOSE, BOREHAMWOOD
            "10034165002",  # 77 ALLUM LANE, ELSTREE, BOREHAMWOOD
            "10013018262",  # 1 COLDHARBOUR LANE, BUSHEY
            "10013031535",  # KEEPERS LODGE, RECTORY LANE, SHENLEY, RADLETT
            "10013029890",  # KITTS END LODGE, KITTS END ROAD, BARNET
            "10093526495",  # GLASSHOUSE, SOUTH MEDBURN FARM, WATLING STREET, ELSTREE, BOREHAMWOOD
        ]:
            return None

        if record.housepostcode in [
            # split
            "WD25 8BP",
        ]:
            return None
        return super().address_record_to_dict(record)
