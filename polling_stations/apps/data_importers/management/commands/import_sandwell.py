from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAW"
    addresses_name = (
        "2026-05-07/2026-03-17T11:02:02.496814/Democracy_Club__07May2026SANDMBC.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T11:02:02.496814/Democracy_Club__07May2026SANDMBC.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "10008535731",  # 241 PENNCRICKET LANE, ROWLEY REGIS
        ]:
            return None

        if record.addressline6 in [
            # split
            "DY4 7TY",
            "B67 7EP",
            "B64 5RZ",
        ]:
            return None

        return super().address_record_to_dict(record)
