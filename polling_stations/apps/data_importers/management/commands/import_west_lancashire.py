from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLA"
    addresses_name = (
        "2026-05-07/2026-02-05T11:37:28.466200/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-02-05T11:37:28.466200/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    # The following warning can be ignored:
    # WARNING: Polling station Up Holland High School (10662) is in Wigan Metropolitan Borough Council (WGN)
    # but target council is West Lancashire Borough Council (WLA)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012344947",  # 201 SHAW HALL CARAVAN PARK SMITHY LANE, SCARISBRICK
            "10012363964",  # 1 COLLIER WAY, UPHOLLAND, SKELMERSDALE
            "10012363965",  # 2 COLLIER WAY, UPHOLLAND, SKELMERSDALE
            "10012363967",  # 4 COLLIER WAY, UPHOLLAND, SKELMERSDALE
            "10012355457",  # APARTMENT 47, BROOKSIDE, AUGHTON STREET, ORMSKIRK
            "10012360939",  # 1 TOWER VIEW CLOSE, BURSCOUGH, ORMSKIRK
        ]:
            return None

        if record.addressline6 in [
            # split
            "PR9 8FB",
            "L40 6JA",
            "L40 4BX",
            "PR4 6RT",
            "L40 5BE",
            "L39 8SR",
            "WN6 9EN",
            "WN8 7XA",
            "WN6 9QE",
            "PR9 8DH",
            "WN8 6SH",
        ]:
            return None

        return super().address_record_to_dict(record)
