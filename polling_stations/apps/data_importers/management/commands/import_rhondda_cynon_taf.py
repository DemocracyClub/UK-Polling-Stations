from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RCT"
    addresses_name = "2026-09-03/2026-08-07T10:02:46.149348/Democracy Club - Idox_2026-08-07 09-55.csv"
    stations_name = "2026-09-03/2026-08-07T10:02:46.149348/Democracy Club - Idox_2026-08-07 09-55.csv"
    elections = ["2026-09-03"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10001300469",  # 34 CAPEL FARM, TONYREFAIL, PORTH
            "200003777546",  # SIGNALMANS COTTAGE, ELY VALLEY ROAD, YNYSMAERDY, PONTYCLUN
            "200002935304",  # POBL LIVING, 11-11A MILL STREET, PONTYPRIDD
        ]:
            return None

        if record.postcode in [
            # splits
            "CF44 0PD",
            "CF38 1DR",
            "CF37 3BS",
            "CF39 8GD",
            "CF40 2ER",
            "CF39 8FA",
            "CF39 8AT",
            "CF44 8LW",
            "CF44 9DT",
            "CF72 8PH",
            "CF38 2JZ",
            # looks wrong
            "CF37 4BP",
            "CF37 1PS",
        ]:
            return None

        return super().address_record_to_dict(record)
