from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLL"
    addresses_name = "2026-05-07/2026-01-05T14:50:24.242351/walsall_edited_2.csv"
    stations_name = "2026-05-07/2026-01-05T14:50:24.242351/walsall_edited_2.csv"
    elections = ["2026-05-07"]
    # Walsall provided their data directly, and not through their EMS so I had to do some manual changes to the file to get it to play nice with the importer
    # This included adding a polling_station_id column and assigning unique IDs to each station. These IDs will NOT MATCH those in future data since I assigned them myself.
    # That means any fixes to stations here will need to be matched to the correct station using the address or other details, not the ID.

    def station_record_to_dict(self, record):
        # These postcode fixes are awaiting council confirmation
        # # 'Leighswood Childcare Centre, Broadmeadow, Walsall, WS9 8HZ' (id: 1)
        # if record.polling_place_id == "1":
        #     record = record._replace(polling_place_postcode="WS9 8HY")
        # # 'The Church on the Corner, 1 King Charles Avenue, Bentley, Walsall, WS2 0DL' (id: 13)
        # if record.polling_place_id == "13":
        #     record = record._replace(polling_place_postcode="WS2 0DB")
        # # 'Stan Ball Centre, Abbotts Street, Bloxwich, Walsall, WS3 3AZ' (id: 17)
        # if record.polling_place_id == "17":
        #     record = record._replace(polling_place_postcode="WS3 3BW")
        # # 'St. Peters R.C. Church Hall, Harrison Street, Bloxwich, Walsall, WS3 3HP' (id: 18)
        # if record.polling_place_id == "18":
        #     record = record._replace(polling_place_postcode="WS3 3LA")
        # # 'Clayhanger Methodist Church, Clayhanger Lane, Clayhanger, Walsall, WS8 7DT' (id: 33)
        # if record.polling_place_id == "33":
        #     record = record._replace(polling_place_postcode="WS8 7DS")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093461877",  # 3A PERRY STREET, DARLASTON, WEDNESBURY
            "10095683310",  # 42 IRONWORKS ROAD, WALSALL
            "10095683332",  # 20 IRONWORKS ROAD, WALSALL
            "10095683330",  # 40 IRONWORKS ROAD, WALSALL
            "10095683321",  # 31 IRONWORKS ROAD, WALSALL
            "10093460985",  # 45 ROWLAND STREET, WALSALL
        ]:
            return None

        if record.addressline6 in [
            # split
            "WV12 4BZ",
            "WS3 2DX",
            "WS1 3LD",
        ]:
            return None
        return super().address_record_to_dict(record)
