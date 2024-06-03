from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DER"
    addresses_name = (
        "2024-07-04/2024-06-03T10:48:23.993486/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-03T10:48:23.993486/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10071162151",  # 6 CHIMLEY STREET, SPONDON, DERBY
        ]:
            return None

        if record.addressline6 in [
            # split
            "DE21 4HF",
            "DE24 0LU",
            "DE73 6UF",
        ]:
            return None

        return super().address_record_to_dict(record)
