from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEI"
    addresses_name = (
        "2025-05-01/2025-02-27T11:26:57.260394/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-27T11:26:57.260394/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
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
                "10032961622",  # WATERGATE, WIDECOMBE-IN-THE-MOOR, NEWTON ABBOT
                "100041193264",  # EASTWREY NURSERIES, MORETONHAMPSTEAD ROAD, LUSTLEIGH, NEWTON ABBOT
                "10091652689",  # WEST LENDON FARM, TEDBURN ST. MARY, EXETER
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "TQ13 9NW",
            "TQ13 7BU",
            "TQ14 9AZ",
            "TQ13 9YW",
            "EX7 9PL",
            "TQ14 9LZ",
            "TQ14 8NL",
            "TQ12 1HR",
            "TQ14 8FW",
            "TQ14 9AA",
            # suspect
            "TQ14 9GZ",
            "TQ14 8NT",
            "TQ13 9JA",
            "TQ13 9EJ",
            "TQ12 6YG",
            "TQ12 6YE",
            "TQ12 6FB",
            "TQ14 8SG",
        ]:
            return None

        return super().address_record_to_dict(record)
