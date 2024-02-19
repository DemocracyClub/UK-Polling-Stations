from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HNS"
    addresses_name = (
        "2024-05-02/2024-02-26T12:09:32.667037/Democracy_Club__02May2024.csv"
    )
    stations_name = (
        "2024-05-02/2024-02-26T12:09:32.667037/Democracy_Club__02May2024.csv"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090801654",  # FLAT THE QUEENS HEAD 123 HIGH STREET, CRANFORD, HOUNSLOW
        ]:
            return None

        if record.addressline6.replace("\xa0", " ") in [
            # split
            "W4 1TF",
            "TW8 0QS",
            "TW3 3DW",
            "TW4 5HS",
            "TW4 6DH",
            "W4 4EU",
            "TW13 6AB",
        ]:
            return None

        return super().address_record_to_dict(record)
