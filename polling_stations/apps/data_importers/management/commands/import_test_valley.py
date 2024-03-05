from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TES"
    addresses_name = (
        "2024-05-02/2024-03-05T16:26:54.791042/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-05T16:26:54.791042/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000704153",  # WOODLANDS, LOCKES DROVE, PILL HEATH, ANDOVER
        ]:
            return None
        if record.addressline6 in [
            # split
            "SP11 0HB",
            "SO51 6EB",
        ]:
            return None
        return super().address_record_to_dict(record)
