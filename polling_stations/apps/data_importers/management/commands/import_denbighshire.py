from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DEN"
    addresses_name = (
        "2024-05-02/2024-04-10T10:59:19.045149/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-10T10:59:19.045149/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004298031",  # AELWYD UCHA, RHUALLT, ST. ASAPH
        ]:
            return None
        return super().address_record_to_dict(record)
