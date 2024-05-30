from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TUN"
    addresses_name = (
        "2024-07-04/2024-05-30T09:04:15.273966/Democracy_Club__04July2024 (1).CSV"
    )
    stations_name = (
        "2024-07-04/2024-05-30T09:04:15.273966/Democracy_Club__04July2024 (1).CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062544084",  # COURTYARD FLAT, COLEBROOKE, PEMBURY ROAD, TONBRIDGE
            "100062543933",  # COLEBROOKE HOUSE, PEMBURY ROAD, TONBRIDGE
            "100061193913",  # HUNTERS LODGE, PEMBURY ROAD, TONBRIDGE
        ]:
            return None

        if record.addressline6 in [
            # split
            "TN12 6GY",
            "TN3 0HX",
            "TN4 0AB",
            # suspect
            "TN11 0PG",
            "TN18 5AH",
        ]:
            return None

        return super().address_record_to_dict(record)
