from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SWL"
    addresses_name = (
        "2023-05-04/2023-03-13T13:50:50.268451/Democracy Club Swale PS export.csv"
    )
    stations_name = (
        "2023-05-04/2023-03-13T13:50:50.268451/Democracy Club Swale PS export.csv"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if record.housepostcode in [
            # split
            "ME10 2EF",
            "ME10 3TU",
            "ME12 1TF",
            "ME12 2SG",
            # LOOK WRONG
            "ME10 2JH",
            "ME10 2JQ",
        ]:
            return None

        if uprn in [
            "200002533735",  # POPPINGTON BUNGALOW, WHITE HILL, SELLING, FAVERSHAM
        ]:
            return None

        return super().address_record_to_dict(record)
