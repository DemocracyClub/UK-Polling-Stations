from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HNS"
    addresses_name = "2024-07-04/2024-06-03T11:58:49.731218/HNS_combined.csv"
    stations_name = "2024-07-04/2024-06-03T11:58:49.731218/HNS_combined.csv"
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"

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
