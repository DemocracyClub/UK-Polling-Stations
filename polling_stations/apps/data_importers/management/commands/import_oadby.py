from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OAD"
    addresses_name = "2024-05-02/2024-02-23T12:04:52.815246/Democracy_Club__02May2024 (Rev. 22-02-2024).tsv"
    stations_name = "2024-05-02/2024-02-23T12:04:52.815246/Democracy_Club__02May2024 (Rev. 22-02-2024).tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010146840",  # OADBY LODGE FARMHOUSE, GARTREE ROAD, LEICESTER
            "100032050960",  # 109 WELFORD ROAD, WIGSTON
            "100030590752",  # 1 BODMIN AVENUE, WIGSTON
            "10010149302",  # FLAT 1, MOAT HOUSE, 107 MOAT STREET, WIGSTON
            "10010149303",  # FLAT 2, MOAT HOUSE, 107 MOAT STREET, WIGSTON
            "10010149304",  # FLAT 3, MOAT HOUSE, 107 MOAT STREET, WIGSTON
            "10010149305",  # FLAT 4, MOAT HOUSE, 107 MOAT STREET, WIGSTON
            "10010149306",  # FLAT 5, MOAT HOUSE, 107 MOAT STREET, WIGSTON
            "10010149307",  # FLAT 6, MOAT HOUSE, 107 MOAT STREET, WIGSTON
            "10010149308",  # FLAT 7, MOAT HOUSE, 107 MOAT STREET, WIGSTON
            "10010149309",  # FLAT 8, MOAT HOUSE, 107 MOAT STREET, WIGSTON
            "10010149310",  # FLAT 9, MOAT HOUSE, 107 MOAT STREET, WIGSTON
            "100030601417",  # 1 TRURO DRIVE, WIGSTON
            "100030589686",  # MELROSE HOUSE, NEWTON LANE, WIGSTON
        ]:
            return None

        return super().address_record_to_dict(record)
