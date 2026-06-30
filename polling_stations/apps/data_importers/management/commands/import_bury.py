from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUR"
    addresses_name = (
        "2026-07-30/2026-06-30T11:45:52.627463/Democracy_Club__30July2026.CSV"
    )
    stations_name = (
        "2026-07-30/2026-06-30T11:45:52.627463/Democracy_Club__30July2026.CSV"
    )
    elections = ["2026-07-30"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "4210011016",  # BIRCHEM BOWER FARM, HARWOOD ROAD, TOTTINGTON, BURY
            "100010966697",  # MANSONS, 10 MANCHESTER OLD ROAD, BURY
        ]:
            return None

        if record.addressline6 in [
            # split
            "BL8 2HH",
            "BL9 7PW",
            "BL9 8JJ",
            "BL9 8JW",
            "BL9 9JW",
            "BL9 9PQ",
            "M25 1JW",
            # suspect
            "BL8 1TF",
            "BL8 4LB",
            "BL8 3HL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Postcode correction for: Chapelfield CP School, Clough Street, Radcliffe, M26 9LH
        if record.polling_place_id == "6462":
            record = record._replace(polling_place_postcode="M26 1LH")

        return super().station_record_to_dict(record)
