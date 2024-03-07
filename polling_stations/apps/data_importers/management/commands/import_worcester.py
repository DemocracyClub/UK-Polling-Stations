from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOC"
    addresses_name = (
        "2024-05-02/2024-03-07T14:51:40.893421/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-07T14:51:40.893421/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]
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
