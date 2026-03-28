from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIN"
    addresses_name = (
        "2026-05-07/2026-03-13T16:23:55.180820/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-13T16:23:55.180820/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "100062518967",  # 16 LIME CLOSE, COLDEN COMMON, WINCHESTER
            "100060605297",  # 18 LIME CLOSE, COLDEN COMMON, WINCHESTER
            "10090845084",  # FLAT 8, 4 ST, CROSS ROAD, WINCHESTER
            "100060612001",  # SILWOOD LODGE, STOCKBRIDGE ROAD, WINCHESTER
        ]:
            return None

        if record.post_code in [
            # splits
            "SO24 9HZ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # WARNING: Polling station Upham New Millennium Village Hall is in Eastleigh Borough Council (EAT)
        # moving pin to the hall and within council boundries (small change)
        # Swanmore Village Hall (Main Hall), New Road, Swanmore, SO32 2PF
        if record.polling_place_id == "12409":
            record = record._replace(
                polling_place_easting="452216", polling_place_northing="119578"
            )
        return super().station_record_to_dict(record)
