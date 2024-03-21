from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BEX"
    addresses_name = (
        "2024-05-02/2024-03-21T10:27:21.289250/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-21T10:27:21.289250/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094789367",  # 51A MAYPLACE ROAD WEST, BEXLEYHEATH
            "10094791073",  # 2C GRANVILLE ROAD, SIDCUP
            "10094790360",  # 1 FEN GROVE, SIDCUP
            "100020267460",  # 69 CUMBERLAND AVENUE, WELLING
        ]:
            return None

        if record.addressline6 in [
            "DA16 2QP",  # split
            # suspect
            "DA14 6NE",  # LAWRENCE COURT, SIDCUP
        ]:
            return None
        return super().address_record_to_dict(record)
