from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DAL"
    addresses_name = (
        "2024-05-02/2024-03-25T17:20:18.000995/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-25T17:20:18.000995/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10003079870",  # LIMEKILN COTTAGE, PIERCEBRIDGE, DARLINGTON
        ]:
            return None

        if record.addressline6 in [
            # split
            "DL1 2RG",
        ]:
            return None

        return super().address_record_to_dict(record)
