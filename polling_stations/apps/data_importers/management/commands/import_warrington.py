from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRT"
    addresses_name = "2024-07-04/2024-06-14T13:23:35.081082/WRT_combined.tsv"
    stations_name = "2024-07-04/2024-06-14T13:23:35.081082/WRT_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Woolston Social Club, 50 Manchester Road, Woolston, Warrington
        if record.polling_place_id == "3224":
            record = record._replace(
                polling_place_easting="364031",
                polling_place_northing="389256",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "200000979589",  # CULCHETH VET SURGERY, 487 WARRINGTON ROAD, CULCHETH, WARRINGTON
                "10094964210",  # 1 SWANICK WAY, WARRINGTON
                "200000985719",  # 37A WINWICK STREET, WARRINGTON
                "10094964692",  # 14 WESTON PARK DRIVE, WARRINGTON
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "WA4 5PQ",
            "WA4 1UN",
            "WA5 9YX",
            "WA2 0RT",
            # suspect
            "WA5 3BF",
        ]:
            return None
        return super().address_record_to_dict(record)
