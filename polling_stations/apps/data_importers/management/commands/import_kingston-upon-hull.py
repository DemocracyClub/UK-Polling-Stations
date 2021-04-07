from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KHL"
    addresses_name = "2021-03-22T11:42:17.468986/Hull Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-22T11:42:17.468986/Hull Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "21130823",  # MANAGERS FLAT THE OLD ZOOLOGICAL PUBLIC HOUSE PRINCES AVENUE, KINGSTON UPON HULL
            "21130822",  # ASSISTANT MANAGERS FLAT THE OLD ZOOLOGICAL PUBLIC HOUSE PRINCES AVENUE, KINGSTON UPON HULL
            "10091482470",  # 332B SOUTHCOATES LANE, KINGSTON UPON HULL
            "10091482471",  # 332C SOUTHCOATES LANE, KINGSTON UPON HULL
        ]:
            return None

        if record.addressline6 in [
            "HU5 3LT",
            "HU9 4HN",
            "HU5 2RH",
            "HU3 6AB",
            "HU7 4ZE",
            "HU5 5NT",
        ]:
            return None

        return super().address_record_to_dict(record)
