from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KHL"
    addresses_name = (
        "2023-05-04/2023-03-16T11:46:29.845477/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-16T11:46:29.845477/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "21130823",  # MANAGERS FLAT THE OLD ZOOLOGICAL PUBLIC HOUSE PRINCES AVENUE, KINGSTON UPON HULL
        ]:
            return None

        if record.addressline6 in [
            # split
            "HU5 2RH",
            "HU5 3LT",
            "HU5 5NT",
        ]:
            return None

        return super().address_record_to_dict(record)
