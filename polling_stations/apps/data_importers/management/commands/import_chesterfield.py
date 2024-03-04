from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHS"
    addresses_name = (
        "2024-05-02/2024-03-04T13:24:25.268238/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-04T13:24:25.268238/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "74068238",  # THE PADDOCKS, CROW LANE, CHESTERFIELD
            "74006059",  # DOBBIN CLOUGH FARM, CROW LANE, CHESTERFIELD
            "74078771",  # 84 SALTERGATE, CHESTERFIELD
            "74026116",  # HILL TOP, HALL LANE, STAVELEY, CHESTERFIELD
        ]:
            return None

        if record.addressline6 in [
            # split
            "S40 3LA",
            # suspect
            "S40 2AL",
        ]:
            return None

        return super().address_record_to_dict(record)
