from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWL"
    addresses_name = (
        "2025-05-01/2025-03-24T11:11:48.525799/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-24T11:11:48.525799/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "200003503741",  # OLD FARMHOUSE, NOTTINGHAM ROAD, STAUNTON HAROLD, ASHBY-DE-LA-ZOUCH
                "10002361080",  # KEEPERS COTTAGE, KEGWORTH LANE, LONG WHATTON, LOUGHBOROUGH
                "200003505244",  # THE AVIARY, WARREN LANE, WHITWICK, COALVILLE
                "10002353672",  # THE MALTINGS, STATION ROAD, HUGGLESCOTE, COALVILLE
                "10002361801",  # FLAT 1, SHELLBROOK HOUSE IC, MARKET STREET, ASHBY-DE-LA-ZOUCH
                "100030551333",  # 68 BURTON ROAD, ASHBY-DE-LA-ZOUCH
                "10095742061",  # FINCH HOUSE, LOWER MOOR ROAD, COLEORTON, COALVILLE
                "100030568246",  # HOO ASH BUNGALOW, SWANNINGTON ROAD, COALVILLE
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "DE74 2DE",
        ]:
            return None

        return super().address_record_to_dict(record)
