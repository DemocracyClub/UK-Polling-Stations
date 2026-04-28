from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DGY"
    addresses_name = "2026-05-07/2026-04-02T11:06:45.484130/DGY_districts_UTF8.csv"
    stations_name = "2026-05-07/2026-04-02T11:06:45.484130/D&G Democracy Counts - Polling Stations 250326.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # Coord fix verified by council for:
        # THORNHILL COMMUNITY CENTRE, EAST BACK STREET, DG3 5LH
        if record.stationcode in ["DFS11", "DFS10"]:
            record = record._replace(
                xordinate="287817",
                yordinate="595787",
            )

        # remove point for BALMAGHIE PUBLIC HALL
        # https://wheredoivote.co.uk/admin/bug_reports/bugreport/786/change/
        if record.stationcode in ["GWD37"]:
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
