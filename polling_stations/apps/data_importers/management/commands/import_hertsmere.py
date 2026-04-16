from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "HER"
    addresses_name = "2026-05-07/2026-04-16T16:06:49.796948/Democracy Club - Idox_2026-04-16 16-06.csv"
    stations_name = "2026-05-07/2026-04-16T16:06:49.796948/Democracy Club - Idox_2026-04-16 16-06.csv"
    elections = ["2026-05-07"]

    # Commented out temporarily for a by-election

    # # Following warnings checked and no need for correction:
    # # WARNING: Polling station MERIDEN COMMUNITY CENTRE (18-meriden-community-centre) is in Watford Borough Council (WAT)

    # def address_record_to_dict(self, record):
    #     uprn = record.uprn.strip().lstrip("0")

    #     if (
    #         uprn
    #         in [
    #             "10013031843",  # SOUTH LODGE, BLACKHORSE LANE, SOUTH MIMMS, POTTERS BAR
    #             "10034171504",  # SHENLEY LODGE COTTAGE MANOR LODGE SCHOOL RIDGE HILL, SHENLEY
    #             "10034165002",  # 77 ALLUM LANE, ELSTREE, BOREHAMWOOD
    #         ]
    #     ):
    #         return None

    #     if record.housepostcode in [
    #         # split
    #         "WD25 8BP",
    #     ]:
    #         return None
    #     return super().address_record_to_dict(record)
