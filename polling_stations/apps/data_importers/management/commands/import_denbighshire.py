from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DEN"
    addresses_name = "2026-06-25/2026-06-08T12:46:18.760688/merged.tsv"
    stations_name = "2026-06-25/2026-06-08T12:46:18.760688/merged.tsv"
    elections = ["2026-06-25"]
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
