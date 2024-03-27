from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GRE"
    addresses_name = (
        "2024-05-02/2024-03-27T13:53:47.769704/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-27T13:53:47.769704/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100020975456",  # 56A HILLREACH, LONDON
        ]:
            return None

        if record.addressline6 in [
            # split
            "SE3 9BT",
            "SE9 2BU",
        ]:
            return None
        return super().address_record_to_dict(record)
