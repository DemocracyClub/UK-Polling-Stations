from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOL"
    addresses_name = (
        "2026-05-07/2026-03-18T18:14:44.914330/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-18T18:14:44.914330/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.lstrip("0")

        if uprn in [
            "100070956066",  # 1 ST. JOHNS GROVE, BIRMINGHAM
            "100071341544",  # WILLOW COTTAGE, WOOTTON LANE, BALSALL COMMON, COVENTRY
        ]:
            return None

        if record.addressline6 in [
            # split
            "B92 8NA",
            "B90 3EE",
            "B37 7RN",
            "B90 4DP",
            "B36 0UD",
        ]:
            return None

        return super().address_record_to_dict(record)
