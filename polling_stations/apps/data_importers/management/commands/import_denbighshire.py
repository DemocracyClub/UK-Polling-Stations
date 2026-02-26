from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DEN"
    addresses_name = (
        "2026-05-07/2026-02-26T14:09:17.885169/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-26T14:09:17.885169/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004298031",  # AELWYD UCHA, RHUALLT, ST. ASAPH
            "200004299740",  # YR HEN FELIN, LLANNEFYDD ROAD, HENLLAN, DENBIGH
        ]:
            return None

        if record.addressline6 in [
            # suspect
            "LL15 1FF",
            "LL18 3AG",
        ]:
            return None

        return super().address_record_to_dict(record)
