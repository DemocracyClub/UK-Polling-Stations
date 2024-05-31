from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAA"
    addresses_name = (
        "2024-07-04/2024-05-31T22:39:36.717310/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-31T22:39:36.717310/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100060449180",  # 161A WEST LANE, HAYLING ISLAND
            "100060449181",  # 161 WEST LANE, HAYLING ISLAND
        ]:
            return None

        if record.addressline6 in [
            # splits
            "PO9 4JG",
        ]:
            return None

        return super().address_record_to_dict(record)
