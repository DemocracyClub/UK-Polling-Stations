from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIN"
    addresses_name = (
        "2025-05-01/2025-03-03T12:53:26.504295/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-03T12:53:26.504295/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10033831876",  # THE STABLES, DESFORD LANE, RATBY, LEICESTER"
            "10033728621",  # BARWELL SPORTS BAR, KIRKBY ROAD, BARWELL, LEICESTER
            "100030503769",  # 10 HILL STREET, BARWELL
        ]:
            return None

        if record.addressline6 in [
            # split
            "LE10 2GJ",
            "LE10 0QL",
            "LE9 8JA",
            "CV13 6LR",
            # suspect
            "LE10 1SS",
            "LE10 1SR",
        ]:
            return None
        return super().address_record_to_dict(record)
