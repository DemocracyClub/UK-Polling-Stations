from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIN"
    addresses_name = (
        "2024-07-04/2024-05-30T13:01:47.936798/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-05-30T13:01:47.936798/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

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
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Markfield Community and Sports Centre - Small Hall, Mayflower Close, Markfield, Leics
        if record.polling_place_id == "4943":
            record = record._replace(
                polling_place_easting="449061", polling_place_northing="309845"
            )
        return super().station_record_to_dict(record)
