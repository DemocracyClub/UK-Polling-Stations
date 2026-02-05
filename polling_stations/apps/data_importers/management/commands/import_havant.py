from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAA"
    addresses_name = (
        "2026-05-07/2026-02-05T14:04:29.515690/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-05T14:04:29.515690/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013686452",  # THE ANNEXE 2 LOVEDEAN LANE, WATERLOOVILLE
            "10013687155",  # ANNEXE 30 FIR COPSE ROAD, WATERLOOVILLE
            "100060455188",  # 129 LONDON ROAD, WATERLOOVILLE
        ]:
            return None

        if record.addressline6 in [
            "PO9 4JG",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
