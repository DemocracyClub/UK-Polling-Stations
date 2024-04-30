from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NKE"
    addresses_name = (
        "2024-05-02/2024-03-04T16:20:03.322219/Democracy_Club__02May2024 (8).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-04T16:20:03.322219/Democracy_Club__02May2024 (8).tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "LN4 1EP",
            "NG34 8AA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Station change requested by council:
        # OLD: Silk Willoughby Village Hall, School Lane, Silk Willoughby, Sleaford, NG34 8PG
        # NEW: St Denis Church, Church Lane, Silk Willoughby, NG34 8PD
        if record.polling_place_id == "8254":
            record = record._replace(
                polling_place_name="St Denis Church",
                polling_place_address_1="Church Lane",
                polling_place_address_2="Silk Willoughby",
                polling_place_address_3="",
                polling_place_address_4="",
                polling_place_postcode="NG34 8PD",
                polling_place_easting="",
                polling_place_northing="",
            )

        return super().station_record_to_dict(record)
