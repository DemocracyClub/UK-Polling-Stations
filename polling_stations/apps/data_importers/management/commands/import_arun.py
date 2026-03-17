from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ARU"
    addresses_name = (
        "2026-05-07/2026-03-17T14:10:45.199004/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T14:10:45.199004/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10023374366",  # CORNERWAYS APARTMENT, WEAVERS HILL, ANGMERING, LITTLEHAMPTON
                "100061728945",  # THE MALTHOUSE, WEAVERS HILL, ANGMERING, LITTLEHAMPTON
                "10091567667",  # 7 WEST MEADS DRIVE, BOGNOR REGIS
                "100062611104",  # 99 HEWARTS LANE, BOGNOR REGIS
                "100061691444",  # PINECROFT STABLES 7A COPTHORNE WAY, ALDWICK
                "100062611104",  # 99 HEWARTS LANE, BOGNOR REGIS
            ]
        ):
            return None

        if record.addressline6 in [
            # looks wrong
            "BN16 4QT",
            "BN16 4QZ",
            "PO22 8GE",
            "PO22 8GD",
            "PO22 8GF",
            "PO22 8GB",
            "PO22 8GQ",
            "PO22 8GP",
        ]:
            return None

        return super().address_record_to_dict(record)
