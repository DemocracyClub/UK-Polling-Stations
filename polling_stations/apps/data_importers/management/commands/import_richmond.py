from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RIC"
    addresses_name = (
        "2024-05-02/2024-04-03T14:23:15.057604/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-03T14:23:15.057604/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "10094588154",  # 42 ROSSLYN AVENUE, LONDON
        ]:
            return None
        if record.addressline6 in [
            # split
            "TW2 5NJ",
            "TW12 2SB",
        ]:
            return None
        return super().address_record_to_dict(record)
