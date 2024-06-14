from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DEN"
    addresses_name = (
        "2024-07-04/2024-06-14T15:02:30.247466/Democracy_Club__04July2024 (28).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-14T15:02:30.247466/Democracy_Club__04July2024 (28).tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004298031",  # AELWYD UCHA, RHUALLT, ST. ASAPH
            "10003928367",  # MYNYDD LLANFAIR, BRYNEGLWYS, CORWEN
        ]:
            return None

        if record.addressline6 in [
            # suspect
            "LL15 1FF",
        ]:
            return None

        return super().address_record_to_dict(record)
