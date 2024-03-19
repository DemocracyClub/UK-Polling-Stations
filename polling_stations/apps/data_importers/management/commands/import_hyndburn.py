from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HYN"
    addresses_name = (
        "2024-05-02/2024-03-19T16:59:46.456514/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-19T16:59:46.456514/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10009967792",  # 3 HIGH STREET, ACCRINGTON
            "100012878207",  # LEG LOCK FARM, SOUGH LANE, GUIDE, BLACKBURN
        ]:
            return None
        if record.addressline6 in [
            "BB5 5QA",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
