from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TES"
    addresses_name = (
        "2024-07-04/2024-05-28T20:43:41.926480/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T20:43:41.926480/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
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
