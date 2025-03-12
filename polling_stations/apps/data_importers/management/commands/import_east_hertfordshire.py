from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EHE"
    addresses_name = (
        "2025-05-01/2025-03-24T12:39:42.372250/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-24T12:39:42.372250/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034624304",  # JACOB NEURO CENTRE, HIGH WYCH ROAD, SAWBRIDGEWORTH
            "10094847645",  # 18 GROSVENOR WALK, HERTFORD
            "10033105209",  # BEECHCROFT, STANDON GREEN END, HIGH CROSS, WARE
            "200002751708",  # PARK HOUSE, THE DRIVE, SAWBRIDGEWORTH
            "10033100497",  # MARLERS, PYE CORNER, GILSTON, HARLOW
            "10023090473",  # MARLERS LODGE, PYE CORNER, GILSTON, HARLOW
            "10034515380",  # 103 GILSTON, HARLOW
            "10034515381",  # 104 GILSTON, HARLOW
        ]:
            return None

        if record.addressline6 in [
            # split
            "AL6 0LJ",
            "SG9 9DW",
            # look wrong
            "SG12 0XY",
            "CM23 2EG",
            "CM23 4SA",
            "SG14 1FU",
            "SG13 7BE",
            "SG13 7BF",
            "SG14 2PQ",
            "SG14 1FT",
            "CM23 4SB",
            "CM23 0AS",
            "CM23 0AH",
            "CM23 0AR",
        ]:
            return None
        return super().address_record_to_dict(record)
