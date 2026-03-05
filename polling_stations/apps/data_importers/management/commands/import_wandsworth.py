from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WND"
    addresses_name = (
        "2026-05-07/2026-03-05T16:23:21.565444/Democracy_Club__07May2026 (2).tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-05T16:23:21.565444/Democracy_Club__07May2026 (2).tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100022701958",  # 5 THURLEIGH MANSIONS 33 THURLEIGH ROAD, LONDON
            "100023328601",  # THE COTTAGE, MAGDALEN ROAD, LONDON
        ]:
            return None

        if record.addressline6 in [
            # split
            "SW12 9RF",
        ]:
            return None

        return super().address_record_to_dict(record)
