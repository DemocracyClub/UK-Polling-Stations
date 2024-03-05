from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HUN"
    addresses_name = (
        "2024-05-02/2024-03-05T14:28:58.853244/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-05T14:28:58.853244/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in []:
            return None

        if record.addressline6 in [
            # split
            "PE19 1HW",
            "PE28 2QG",
            "PE27 6DT",
            # suspect
            "PE29 1NY",
            "PE28 4NS",
            "PE28 4EW",
        ]:
            return None

        return super().address_record_to_dict(record)
