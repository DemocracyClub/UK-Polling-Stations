from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEI"
    addresses_name = "2024-07-04/2024-05-28T13:19:59.695770/TeignbridgeDemocracy_Club__04July2024.tsv"
    stations_name = "2024-07-04/2024-05-28T13:19:59.695770/TeignbridgeDemocracy_Club__04July2024.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10032954133",  # BARN COTTAGE, HIGHER BRIMLEY, BOVEY TRACEY, NEWTON ABBOT
                "100041145017",  # GLENDARAGH, EXETER ROAD, DAWLISH
                "10032961123",  # WEST LODGE HEDGE BARTON, WIDECOMBE-IN-THE-MOOR, NEWTON ABBOT
                "10032961778",  # TREETOPS, HIGHER ASHTON, EXETER
                "10032961361",  # HIGHER BRAKE, HAYTOR, NEWTON ABBOT
                "100040322956",  # BROCKS WAY, GREEN LANE, ILSINGTON, NEWTON ABBOT
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "TQ13 9YW",
            "TQ12 1HR",
            "TQ14 8FW",
            "TQ13 7BU",
            "TQ14 9LZ",
            "TQ14 9AA",
            "TQ14 8NL",
            "EX7 9PL",
            "TQ13 9NW",
            # suspect
            "TQ14 9EP",
            "TQ14 9GZ",
            "TQ14 8NT",
            "TQ13 9JA",
            "TQ13 9EJ",
            "TQ12 6YG",
            "TQ12 6YE",
        ]:
            return None

        return super().address_record_to_dict(record)
