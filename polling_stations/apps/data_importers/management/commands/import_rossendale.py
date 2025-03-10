from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROS"
    addresses_name = (
        "2025-05-01/2025-03-10T10:56:30.669919/Democracy_Club__01May2025 (4).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-10T10:56:30.669919/Democracy_Club__01May2025 (4).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100012410998",  # HEIGHT END FARM, HASLINGDEN OLD ROAD, ROSSENDALE
            "100012410082",  # 1A ROCHDALE ROAD, RAMSBOTTOM, BURY
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BB4 8TT",
            # suspect
            "BB4 9QR",
        ]:
            return None

        return super().address_record_to_dict(record)
