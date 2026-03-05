from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "CHO"
    addresses_name = "2026-05-07/2026-03-05T10:44:32.194903/Democracy Club - Idox_2026-03-05 10-36.csv"
    stations_name = "2026-05-07/2026-03-05T10:44:32.194903/Democracy Club - Idox_2026-03-05 10-36.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100010387618",  # MILLSTONE HOUSE, THE GREEN, ECCLESTON, CHORLEY
        ]:
            return None

        if record.postcode in [
            # split
            "PR6 0HT",
            "PR7 2QL",
            # suspect
            "PR26 9HE",
        ]:
            return None

        return super().address_record_to_dict(record)
