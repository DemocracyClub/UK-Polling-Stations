from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THR"
    addresses_name = (
        "2024-05-02/2024-03-18T15:41:44.781816/Democracy_Club__02May2024 (22).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-18T15:41:44.781816/Democracy_Club__02May2024 (22).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095907154",  # 1A HIGH STREET, GRAYS
            "200001546102",  # LANGDON HALL FARM, OLD CHURCH HILL, LANGDON HILLS, BASILDON
            "100091297522",  # BENTLEY FARM, OLD CHURCH HILL, LANGDON HILLS, BASILDON
            "100091297871",  # HOB HILL FARM, BIGGIN LANE, GRAYS
        ]:
            return None

        if record.addressline6.strip() in [
            # splits
            "RM19 1QJ",
            "RM16 4RB",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
