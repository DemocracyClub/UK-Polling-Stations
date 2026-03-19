from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLA"
    addresses_name = (
        "2026-05-07/2026-03-06T13:01:56.827249/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-06T13:01:56.827249/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    # The following warning can be ignored:
    # WARNING: Polling station Up Holland High School (11265) is in Wigan Metropolitan Borough Council (WGN)
    # but target council is West Lancashire Borough Council (WLA)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012368707",  # 3 AUGHTON STREET, ORMSKIRK, L39 3BH
            "10012361854",  # 1 JOYFORD CLOSE, SKELMERSDALE, WN8 6GX
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
            "L40 4BX",
            "L40 5BE",
            "L39 8SR",
            "PR4 6RT",
            "WN8 6SH",
            "L40 6JA",
            "PR9 8FB",
            "WN8 7XA",
            "PR9 8DH",
            "WN6 9QE",
            "WN6 9EN",
            # looks wrong
            "PR9 8DF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: St Francis of Assisi Church, Beechtrees, Skelmersdale
        if record.polling_place_id == "11535":
            record = record._replace(polling_place_postcode="WN8 9ET")

        return super().station_record_to_dict(record)
