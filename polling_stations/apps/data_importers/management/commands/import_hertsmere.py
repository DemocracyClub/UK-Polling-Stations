from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "HER"
    addresses_name = "2025-05-01/2025-03-12T17:07:55.818621/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-03-12T17:07:55.818621/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]

    # Following warnings checked and no need for correction:
    # WARNING: Polling station MERIDEN COMMUNITY CENTRE (18-meriden-community-centre) is in Watford Borough Council (WAT)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10013031843",  # SOUTH LODGE, BLACKHORSE LANE, SOUTH MIMMS, POTTERS BAR
                "10034171504",  # SHENLEY LODGE COTTAGE MANOR LODGE SCHOOL RIDGE HILL, SHENLEY
                "10034165002",  # 77 ALLUM LANE, ELSTREE, BOREHAMWOOD
            ]
        ):
            return None

        if record.housepostcode in [
            # split
            "WD25 8BP",
        ]:
            return None
        return super().address_record_to_dict(record)
