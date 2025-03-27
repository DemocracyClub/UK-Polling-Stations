from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLA"
    addresses_name = (
        "2025-05-01/2025-03-27T10:21:21.955308/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-27T10:21:21.955308/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]

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
            "WN6 9EN",
            "L39 8SR",
            "PR4 6RT",
            "WN6 9QE",
            "L40 6JA",
            "L40 5BE",
            "PR9 8FB",
            "WN8 6SH",
            "WN8 7XA",
            "PR9 8DH",
        ]:
            return None

        return super().address_record_to_dict(record)
