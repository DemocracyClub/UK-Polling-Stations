from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "AGY"
    addresses_name = "2026-05-07/2026-03-05T16:31:00.410075/Democracy Club - Idox_2026-03-05 15-54.csv"
    stations_name = "2026-05-07/2026-03-05T16:31:00.410075/Democracy Club - Idox_2026-03-05 15-54.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "LL65 2ED",
            "LL77 7NW",
            "LL65 2EL",
            "LL65 1BG",
            "LL74 8ST",
            "LL72 8LJ",
        ]:
            return None

        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002649098",  # 4 TREMWYLFA, CARMEL, LLANNERCH-Y-MEDD
            "10024357287",  # CHAPEL HOUSE, SOUTH STACK ROAD, HOLYHEAD
            "10013463367",  # HARBOUR HOUSE, TRAETH BYCHAN, MARIANGLAS
            "10013466388",  # OLD GRANARY, PENTRAETH
            "10013853106",  # PANT Y BWLCH, LLANDDONA, BEAUMARIS
            "10013466115",  # RHANDIR, LLANFIGAEL, HOLYHEAD
        ]:
            return None

        return super().address_record_to_dict(record)
