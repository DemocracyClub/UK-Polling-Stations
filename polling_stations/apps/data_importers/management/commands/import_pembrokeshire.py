from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "PEM"
    addresses_name = "2026-05-07/2026-02-17T13:17:53.759530/Democracy Club - Idox_2026-02-16 14-31.csv"
    stations_name = "2026-05-07/2026-02-17T13:17:53.759530/Democracy Club - Idox_2026-02-16 14-31.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        record.uprn.strip().lstrip("0")
        if record.uprn in [
            "10013172306",  # HILLFORT PRIORYRATH, HOWARTH CLOSE, MILFORD HAVEN
        ]:
            return None
        if record.postcode in [
            # split
            "SA62 4NJ",
            "SA73 3RA",
            "SA62 3DA",
            "SA62 5RJ",
            "SA62 3PW",
            "SA71 5BP",
            "SA73 1RG",
            "SA73 1BB",
            "SA71 4BP",
            "SA73 1RJ",
            "SA68 0QR",
            "SA72 6BH",
            "SA72 6BE",
            "SA73 3HF",
            "SA73 2EB",
            "SA62 6TD",
            "SA42 0QG",
            "SA73 1BL",
            "SA68 0XN",
            "SA73 1NR",
            "SA67 8RY",
            "SA62 5UD",
            "SA66 7QW",
            "SA62 5DB",
            "SA62 5NL",
            "SA71 4JT",
        ]:
            return None
        return super().address_record_to_dict(record)
