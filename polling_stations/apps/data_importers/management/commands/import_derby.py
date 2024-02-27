from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DER"
    addresses_name = (
        "2024-05-02/2024-02-27T15:37:31.914168/Democracy_Club__02May2024 Derby.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-27T15:37:31.914168/Democracy_Club__02May2024 Derby.tsv"
    )
    elections = ["2024-05-02"]
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
