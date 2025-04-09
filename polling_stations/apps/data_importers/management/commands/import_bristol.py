from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BST"
    addresses_name = (
        "2025-05-01/2025-03-07T11:57:12.448976/Democracy_Club__01May2025_2025-03-07.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-07T11:57:12.448976/Democracy_Club__01May2025_2025-03-07.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "310372",  # THE BUNGALOW, GOLF COURSE LANE, BRISTOL
        ]:
            return None

        if record.post_code in [
            # split
            "BS7 8JP",
            # suspect
            "BS14 0SW",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Station Change from councl:
        # Old: Lawrence Weston Youth Centre, Lawrence Weston Road, Lawrence Weston, Bristol BS11 0RX
        # New:The Rock Community Centre, St Peter's Church, Ridingleaze, Lawrence Weston, Bristol BS11 0QF 31897
        if record.polling_place_id == "31901":
            record = record._replace(
                polling_place_name="The Rock Community Centre",
                polling_place_address_1="St Peter's Church",
                polling_place_address_2="Ridingleaze",
                polling_place_address_3="Lawrence Weston",
                polling_place_address_4="Bristol",
                polling_place_postcode="BS11 0QF",
            )

        return super().station_record_to_dict(record)
