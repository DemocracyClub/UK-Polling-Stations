from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUR"
    addresses_name = (
        "2026-05-07/2026-03-04T17:09:50.640643/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-04T17:09:50.640643/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "4210011016",  # BIRCHEM BOWER FARM, HARWOOD ROAD, TOTTINGTON, BURY
            "100010966697",  # MANSONS, 10 MANCHESTER OLD ROAD, BURY
        ]:
            return None

        if record.addressline6 in [
            # split
            "BL9 9JW",
            "BL9 8JJ",
            "BL9 7PW",
            "M25 1JW",
            "BL8 2HH",
            "BL9 9PQ",
            "BL9 8JW",
            # suspect
            "BL8 1TF",
            "BL8 4LB",
            "BL8 3HL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Postcode correction for: Chapelfield CP School, Clough Street, Radcliffe, M26 9LH
        if record.polling_place_id == "6005":
            record = record._replace(polling_place_postcode="M26 1LH")

        return super().station_record_to_dict(record)
