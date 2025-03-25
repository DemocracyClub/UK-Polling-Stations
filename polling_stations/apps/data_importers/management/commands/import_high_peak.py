from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIG"
    addresses_name = (
        "2025-05-01/2025-03-25T10:11:00.608557/Democracy_Club__01May2025 (5).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-25T10:11:00.608557/Democracy_Club__01May2025 (5).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10010727932",  # HOCKERLEY HALL FARM, HOCKERLEY LANE, WHALEY BRIDGE, HIGH PEAK
                "10010747214",  # THE BUNGALOW, HARPUR HILL BUSINESS PARK, BUXTON
                "10010715355",  # RED GAP FARM, GREEN FAIRFIELD, BUXTON
                "10010751272",  # MILTON FARMHOUSE, CHAPEL MILTON, CHAPEL-EN-LE-FRITH, HIGH PEAK
                "10010729164",  # BROOK COTTAGE, CHAPEL-EN-LE-FRITH, HIGH PEAK
                "10010765701",  # HOLLIN KNOWLE FARM, LONG LANE, CHAPEL-EN-LE-FRITH, HIGH PEAK
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "S33 0AB",
            "SK23 6BR",
            # suspect
            "SK22 3DU",
            "SK22 1BW",
        ]:
            return None

        return super().address_record_to_dict(record)
