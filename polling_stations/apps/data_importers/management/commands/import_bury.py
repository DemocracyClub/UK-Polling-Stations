from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUR"
    addresses_name = (
        "2024-07-04/2024-05-23T17:32:53.988362/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-05-23T17:32:53.988362/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "4210011016",  # BIRCHEM BOWER FARM, HARWOOD ROAD, TOTTINGTON, BURY
            "100010966697",  # MANSONS, 10 MANCHESTER OLD ROAD, BURY
        ]:
            return None

        if record.addressline6 in [
            # split
            "M25 1ED",
            "BL9 8JJ",
            "M25 1JW",
            "BL9 9PQ",
            "BL9 8JW",
            "BL9 9JW",
            "BL8 2HH",
            # suspect
            "BL8 1TF",
            "M26 1RZ",
            "BL8 4LB",
        ]:
            return None

        return super().address_record_to_dict(record)
