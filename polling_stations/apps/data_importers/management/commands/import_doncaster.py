from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DNC"
    addresses_name = (
        "2024-07-04/2024-06-18T10:42:04.528561/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-18T10:42:04.528561/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
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
        ]:
            return None

        if record.addressline6 in [
            # splits
            "DN7 6AQ",
            "DN7 5DG",
            "DN4 7BQ",
            "DN8 5AD",
            "S64 0DE",
            "DN7 6PW",
            "DN3 2AX",
            "DN6 9JU",
            "DN4 8ES",
            "DN5 7DP",
            "S64 0LL",
            "DN5 0QW",
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
