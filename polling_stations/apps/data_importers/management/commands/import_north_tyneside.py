from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NTY"
    addresses_name = (
        "2025-05-01/2025-03-10T17:28:20.212349/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-10T17:28:20.212349/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "47243589",  # 14 BEECH WAY, KILLINGWORTH
            "47070238",  # EAST WIDEOPEN FARM COTTAGE, WIDEOPEN, NEWCASTLE UPON TYNE
            "47014289",  # FLAT ABOVE LOW LIGHTS TAVERN BREWHOUSE BANK, NORTH SHIELDS
            "47049172",  # 83 HOWDON ROAD, NORTH SHIELDS
            "47049170",  # 81 HOWDON ROAD, NORTH SHIELDS
            "47049168",  # 79 HOWDON ROAD, NORTH SHIELDS
            "47229242",  # REDESDALE COURT, RAKE LANE, NORTH SHIELDS
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NE12 8EE",
            # suspect
            "NE28 8AQ",
        ]:
            return None

        return super().address_record_to_dict(record)
