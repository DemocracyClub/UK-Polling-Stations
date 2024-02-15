from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TUN"
    addresses_name = (
        "2024-05-02/2024-02-15T10:01:51.457411/Democracy_Club__02May2024 (1).tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-15T10:01:51.457411/Democracy_Club__02May2024 (1).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

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
            "TN2 5FT",
            "TN4 0AB",
            "TN3 0HX",
            # suspect
            "TN11 0PG",
            "TN18 5AH",
        ]:
            return None

        return super().address_record_to_dict(record)
