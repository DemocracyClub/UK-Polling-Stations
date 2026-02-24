from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "GRT"
    addresses_name = "2026-05-07/2026-02-24T12:43:44.220496/Democracy Club - Idox_2026-02-24 12-26.csv"
    stations_name = "2026-05-07/2026-02-24T12:43:44.220496/Democracy Club - Idox_2026-02-24 12-26.csv"
    elections = ["2026-05-07"]

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

        return super().address_record_to_dict(record)
