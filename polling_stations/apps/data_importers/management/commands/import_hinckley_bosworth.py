from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIN"
    addresses_name = (
        "2023-05-04/2023-04-28T11:19:56.050247/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-04-28T11:19:56.050247/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10033831876",  # THE STABLES, DESFORD LANE, RATBY, LEICESTER
            "10033728621",  # BARWELL SPORTS BAR, KIRKBY ROAD, BARWELL, LEICESTER
            "100030503769",  # 10 HILL STREET, BARWELL
        ]:
            return None

        if record.addressline6 in [
            # split
            "LE10 0QL",
            "LE10 2GJ",
            "LE9 8JA",
            "CV13 6LR",
        ]:
            return None
        return super().address_record_to_dict(record)
