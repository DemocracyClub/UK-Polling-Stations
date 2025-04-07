from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DNC"
    addresses_name = (
        "2025-05-01/2025-04-07T13:03:16.237741/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-07T13:03:16.237741/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10006604850",  # 100A KING EDWARD ROAD, THORNE, DONCASTER
            "100050740021",  # RELAY HOUSE, KING EDWARD ROAD, THORNE, DONCASTER
            "10006574333",  # FIRST FLOOR 187A URBAN ROAD, HEXTHORPE, DONCASTER
            "10095783014",  # BEAWOOD HOUSE, GREAT NORTH ROAD, BAWTRY, DONCASTER
            "100051982929",  # 5 REX CORNER, BROXHOLME LANE, DONCASTER
            "100050726352",  # THE HUGGINS, GATE WOOD LANE, HATFIELD, DONCASTER
            "100050804695",  # CLIFTON CHASE, COMMON LANE, CLIFTON, MALTBY, ROTHERHAM
            "10094838488",  # 80 DONCASTER ROAD, CONISBROUGH, DONCASTER
            "100050704471",  # THE BUNGALOW, BURCROFT HILL, CONISBROUGH, DONCASTER
            "10006712461",  # 41 ORCHARD STREET, THORNE, DONCASTER
            "10006712462",  # 43 ORCHARD STREET, THORNE, DONCASTER
        ]:
            return None

        if record.addressline6 in [
            # splits
            "DN5 0QW",
            "DN6 9JU",
            "DN4 7BQ",
            "S64 0DE",
            "S64 0LL",
            "DN8 5AD",
            "DN7 5DG",
            "DN5 7DP",
            "DN4 8ES",
            "DN3 2AX",
            "DN7 6PW",
            # suspect
            "DN9 3HF",
            "DN4 7AL",
            "DN6 8PX",
            "DN8 4HX",
            "DN8 5TY",
            "DN8 5PA",
        ]:
            return None

        return super().address_record_to_dict(record)
