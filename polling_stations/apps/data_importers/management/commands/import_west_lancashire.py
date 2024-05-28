from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLA"
    addresses_name = (
        "2024-07-04/2024-05-28T16:23:35.023638/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T16:23:35.023638/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    # The following warning can be ignored:
    # WARNING: Polling station Up Holland High School (10662) is in Wigan Metropolitan Borough Council (WGN)
    # but target council is West Lancashire Borough Council (WLA)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012356569",  # 3 THE GRAVEL, MERE BROW, PRESTON
            "10012344947",  # 201 SHAW HALL CARAVAN PARK SMITHY LANE, SCARISBRICK
            "10012365587",  # FLAT 1, HEBA HOUSE, 4 AUGHTON STREET, ORMSKIRK
            "10012363964",  # 1 COLLIER WAY, UPHOLLAND, SKELMERSDALE
            "10012355457",  # APARTMENT 47, BROOKSIDE, AUGHTON STREET, ORMSKIRK
            "10012365587",  # FLAT 1, HEBA HOUSE, 4 AUGHTON STREET, ORMSKIRK
            "10012360939",  # 1 TOWER VIEW CLOSE, BURSCOUGH, ORMSKIRK
            "100012414181",  # ALTYS FARM, ALTYS LANE, ORMSKIRK
        ]:
            return None

        if record.addressline6 in [
            # split
            "L39 8SR",
            "L40 5BE",
            "PR9 8FB",
            "PR4 6RT",
            "WN6 9EN",
            "WN6 9QE",
            "L40 6JA",
            "PR9 8DH",
            "WN8 7XA",
            "WN8 6SH",
        ]:
            return None

        return super().address_record_to_dict(record)
