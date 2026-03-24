from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DGY"
    addresses_name = "2026-05-07/2026-03-24T17:03:44.423040/D&G Democracy Counts - Polling Districts 240326.csv"
    stations_name = "2026-05-07/2026-03-24T17:03:44.423040/D&G Democracy Counts - Polling Stations 240326.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # Removing bad coordinates for:
        # THORNHILL COMMUNITY CENTRE, EAST BACK STREET, DG3 5LH
        if record.stationcode in ["DFS11", "DFS10"]:
            record = record._replace(
                xordinate="0",
                yordinate="0",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "137072115",  # THE STEADING, WALLACETON, AULDGIRTH, DUMFRIES
        ]:
            return None
        if record.postcode in [
            # splits
            "DG5 4HS",
            "DG8 0BZ",
            # suspect
            "DG7 3PF",
            "DG7 3PQ",
        ]:
            return None
        return super().address_record_to_dict(record)
