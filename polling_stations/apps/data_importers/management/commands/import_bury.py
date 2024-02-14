from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUR"
    addresses_name = (
        "2024-05-02/2024-02-14T16:35:28.213398/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-14T16:35:28.213398/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Greenmount Cricket Club, Brandlesholme Road, Bury
        if record.polling_place_id == "4977":
            record = record._replace(polling_place_postcode="BL8 4DX")

        # Tottington Library, Market Street, Tottington
        if record.polling_place_id == "4988":
            record = record._replace(polling_place_postcode="BL8 3LL")

        # Sunnybank Community Centre, 248 Sunnybank Road, Unsworth, Bury
        if record.polling_place_id == "5082":
            record = record._replace(polling_place_postcode="BL9 8EH")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "4210011016",  # BIRCHEM BOWER FARM, HARWOOD ROAD, TOTTINGTON, BURY
            "100010966697",  # MANSONS, 10 MANCHESTER OLD ROAD, BURY
        ]:
            return None

        if record.addressline6 in [
            # split
            "M25 1JW",
            "BL9 8JW",
            "BL8 2HH",
            "BL9 9JW",
            "BL9 8JJ",
            "BL9 9PQ",
            "M25 1ED",
            # suspect
            "BL8 1TF",
            "M26 1RZ",
            "BL8 4LB",
        ]:
            return None

        return super().address_record_to_dict(record)
