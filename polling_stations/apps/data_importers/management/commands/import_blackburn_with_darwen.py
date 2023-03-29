from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BBD"
    addresses_name = (
        "2023-05-04/2023-03-13T10:56:15.307801/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-13T10:56:15.307801/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100012541481",  # DARR CLOTH HOUSE, 5-7 NEW BANK ROAD, BLACKBURN
        ]:
            return None

        if record.addressline6 in [
            # split
            "BB1 7LS",
            "BB3 2NQ",
            "BB1 7LT",
            "BB1 1EB",
            "BB1 2NL",
        ]:
            return None

        return super().address_record_to_dict(record)
