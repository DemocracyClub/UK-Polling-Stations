from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MEL"
    addresses_name = (
        "2025-05-01/2025-03-24T11:04:11.230653/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-24T11:04:11.230653/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "100032044777",  # HILL FARM, EASTWELL ROAD, SCALFORD, MELTON MOWBRAY
            "10095606152",  # BRAMBLE BARN, EASTWELL ROAD, SCALFORD, MELTON MOWBRAY
        ]:
            return None
        if record.addressline6 in [
            # split
            "LE13 1FR",
            "NG32 1QG",
            "LE14 2XB",
            "NG32 1QQ",
            # suspect
            "LE13 0SF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Add missing poostcode for: Freeby Village Hall, Main Street, Freeby, Melton Mowbray
        # Source is from other station in the same bulding (same name/address, ID: 3445)
        if record.polling_place_id == "3413":
            record = record._replace(polling_place_postcode="LE14 2RY")

        return super().station_record_to_dict(record)
