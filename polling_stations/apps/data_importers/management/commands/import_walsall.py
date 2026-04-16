from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLL"
    addresses_name = "2026-05-07/2026-03-09T10:17:51.361198/Walsall Counil. Democracy_Club__07May2026.CSV"
    stations_name = "2026-05-07/2026-03-09T10:17:51.361198/Walsall Counil. Democracy_Club__07May2026.CSV"
    elections = ["2026-05-07"]

    # Council requested to not change below postcodes, we can ignore the warnings
    # 'Leighswood Childcare Centre, Broadmeadow, Walsall, WS9 8HZ'
    # 'The Church on the Corner, 1 King Charles Avenue, Bentley, Walsall, WS2 0DL'
    # 'Stan Ball Centre, Abbotts Street, Bloxwich, Walsall, WS3 3AZ'
    # 'St. Peters R.C. Church Hall, Harrison Street, Bloxwich, Walsall, WS3 3HP'
    # 'Clayhanger Methodist Church, Clayhanger Lane, Clayhanger, Walsall, WS8 7DT'

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

    def station_record_to_dict(self, record):
        # council change for: Metro Inns Walsall, Birmingham Road, Walsall, WS5 3AB
        if record.polling_place_id == "5054":
            record = record._replace(
                polling_place_name="",
                polling_place_address_1="Temp on the corner of Lake Avenue and Cornwall Road",
                polling_place_postcode="",
                polling_place_easting="402844",
                polling_place_northing="297186",
            )

        return super().station_record_to_dict(record)
