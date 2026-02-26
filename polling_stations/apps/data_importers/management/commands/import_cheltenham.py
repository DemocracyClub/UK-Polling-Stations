from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "CHT"
    addresses_name = "2026-05-07/2026-02-26T12:04:00.564616/Democracy Club - Idox_2026-02-24 10-38.csv"
    stations_name = "2026-05-07/2026-02-26T12:04:00.564616/Democracy Club - Idox_2026-02-24 10-38.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002686590",  # HOLMLEA FARM SPRINGBANK ROAD, CHELTENHAM
            "200002686059",  # 3A CLARENCE ROAD, CHELTENHAM
            "100121229562",  # THE MEWS, BACK MONTPELLIER TERRACE, CHELTENHAM
            "200002684616",  # 49A BACK MONTPELLIER TERRACE, CHELTENHAM
            "100120413433",  # FLAT, 19 SUFFOLK ROAD, CHELTENHAM
            "100120399951",  # FARROW & BALL, 15-17 SUFFOLK ROAD, CHELTENHAM
        ]:
            return None

        if record.postcode in [
            # split
            "GL50 2RF",
            "GL52 6RN",
            "GL52 2ES",
            "GL50 3RB",
        ]:
            return None

        return super().address_record_to_dict(record)
