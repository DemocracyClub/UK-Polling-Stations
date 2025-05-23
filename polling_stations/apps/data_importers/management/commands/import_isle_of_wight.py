from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IOW"
    addresses_name = (
        "2025-05-01/2025-04-09T09:59:02.710426/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-09T09:59:02.710426/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"


def address_record_to_dict(self, record):
    uprn = record.property_urn.strip().lstrip("0")

    if uprn in [
        "100060763282",  # 28A HIGH STREET, RYDE
        "10023714741",  # FYNELEA, PRINCES ROAD, FRESHWATER
        "200001868290",  # THE ORCHARDS, PRINCES ROAD, FRESHWATER
        "100062441673",  # WHITE COTTAGE, MILITARY ROAD, ATHERFIELD, VENTNOR
        "200001711156",  # KILN SIDE, NEWPORT ROAD, WHITWELL, VENTNOR
        "200001659225",  # FERNDALE, NEWPORT ROAD, WHITWELL, VENTNOR
        "200001659224",  # BEXHILL COTTAGE, NEWPORT ROAD, WHITWELL, VENTNOR
        "10024249131",  # 34A CASTLE CLOSE, VENTNOR
        "10024249197",  # BATTS LODGE, BATTS ROAD, SHANKLIN
        "10003321336",  # BEACH RETREAT, POND LANE, SEAVIEW
        "10003321335",  # 1 POND LANE, SEAVIEW
        "100060761402",  # CORNERWAYS, BINSTEAD ROAD, RYDE
        "10003318523",  # THE FIELD, MAIN ROAD, HAVENSTREET, RYDE
    ]:
        return None

    return super().address_record_to_dict(record)
