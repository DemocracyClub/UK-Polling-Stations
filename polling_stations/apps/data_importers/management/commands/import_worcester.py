from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOC"
    addresses_name = (
        "2024-07-04/2024-06-03T12:30:53.495756/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-03T12:30:53.495756/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090440987",  # FLAT AT THE BEDWARDINE 128 BROMYARD ROAD, WORCESTER
            "100120648786",  # 145A COLUMBIA DRIVE, WORCESTER
            "10090440987",  # FLAT AT THE BEDWARDINE 128 BROMYARD ROAD, WORCESTER
        ]:
            return None

        if record.addressline6 in [
            "WR5 3EX",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
