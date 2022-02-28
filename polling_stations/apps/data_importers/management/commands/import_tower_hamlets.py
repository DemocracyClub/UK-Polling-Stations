from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TWH"
    addresses_name = (
        "2022-05-05/2022-02-28T09:31:35.482745/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-28T09:31:35.482745/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "6141280",  # FLAT 3 28 CANNON STREET ROAD, LONDON
            "6146893",  # 80B BRUCE ROAD, LONDON
        ]:
            return None
        if record.addressline6 in [
            "E14 0XP",
            "E1 0BH",
            "E14 8EZ",
        ]:
            return None

        return super().address_record_to_dict(record)
