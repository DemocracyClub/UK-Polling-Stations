from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ARU"
    addresses_name = "2024-07-04/2024-06-20T09:50:40.186415/ARU_combined.tsv"
    stations_name = "2024-07-04/2024-06-20T09:50:40.186415/ARU_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023374366",  # CORNERWAYS APARTMENT, WEAVERS HILL, ANGMERING, LITTLEHAMPTON
            "100061728945",  # THE MALTHOUSE, WEAVERS HILL, ANGMERING, LITTLEHAMPTON
            "10023374778",  # THE RANCH, WATER LANE, ANGMERING, LITTLEHAMPTON
            "200002712986",  # 149 SELDEN LANE, PATCHING, WORTHING
            "10091567667",  # 7 WEST MEADS DRIVE, BOGNOR REGIS
            "100061686788",  # SOUTHDOWN COTTAGE, YAPTON LANE, WALBERTON, ARUNDEL
            "200002715229",  # GREEN DOORS LODGE, LONDON ROAD, ARUNDEL
            "100062611104",  # 99 HEWARTS LANE, BOGNOR REGIS
            "100061691444",  # PINECROFT STABLES 7A COPTHORNE WAY, ALDWICK
            "200002712792",  # OLD CHAPEL FORGE, LOWER BOGNOR ROAD, LAGNESS, CHICHESTER
            "100061698125",  # 1 KINGSWAY, BOGNOR REGIS
            "100061713766",  # BROOKENBEE, BROOK LANE, RUSTINGTON, LITTLEHAMPTON
            "200002714870",  # 48 OLD WORTHING ROAD, EAST PRESTON, LITTLEHAMPTON
            "100062611104",  # 99 HEWARTS LANE, BOGNOR REGIS
        ]:
            return None

        if record.addressline6 in [
            # splits
            "PO21 1JB",
            # looks wrong
            "BN16 4QT",
            "BN16 4QZ",
            "PO22 8GE",
            "PO22 8GD",
            "PO22 8GF",
            "PO22 8GB",
            "PO22 8GQ",
            "PO22 8GP",
            "BN18 0YL",
            "BN18 0YN",
            "BN13 3UG",
        ]:
            return None

        return super().address_record_to_dict(record)
