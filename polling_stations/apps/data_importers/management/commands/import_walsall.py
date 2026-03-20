from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLL"
    addresses_name = "2026-05-07/2026-03-09T10:17:51.361198/Walsall Counil. Democracy_Club__07May2026.CSV"
    stations_name = "2026-05-07/2026-03-09T10:17:51.361198/Walsall Counil. Democracy_Club__07May2026.CSV"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # These postcode fixes are areapproved by the council
        # 'Leighswood Childcare Centre, Broadmeadow, Walsall, WS9 8HZ'
        if record.polling_place_id == "4856":
            record = record._replace(polling_place_postcode="WS9 8HY")
        # 'The Church on the Corner, 1 King Charles Avenue, Bentley, Walsall, WS2 0DL'
        if record.polling_place_id == "5006":
            record = record._replace(polling_place_postcode="WS2 0DB")
        # 'Stan Ball Centre, Abbotts Street, Bloxwich, Walsall, WS3 3AZ'
        if record.polling_place_id == "4767":
            record = record._replace(polling_place_postcode="WS3 3BW")
        # 'St. Peters R.C. Church Hall, Harrison Street, Bloxwich, Walsall, WS3 3HP'
        if record.polling_place_id == "4771":
            record = record._replace(polling_place_postcode="WS3 3LA")
        # 'Clayhanger Methodist Church, Clayhanger Lane, Clayhanger, Walsall, WS8 7DT'
        if record.polling_place_id == "4906":
            record = record._replace(polling_place_postcode="WS8 7DS")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10013664361",  # LIVING AREA THE GEORGE STEPHENSON STEPHENSON AVENUE, WALSALL
                "100071031406",  # 65 ALEXANDRA ROAD, WALSALL
                "100071031420",  # 82 ALEXANDRA ROAD, WALSALL
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "WV12 4BZ",
            "WS1 3LD",
            "WS3 2DX",
            # looks wrong
            "WS10 7TG",
        ]:
            return None
        return super().address_record_to_dict(record)
