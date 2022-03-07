from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KHL"
    addresses_name = (
        "2022-05-05/2022-03-07T08:47:17.170429/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-07T08:47:17.170429/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "21130823",  # MANAGERS FLAT THE OLD ZOOLOGICAL PUBLIC HOUSE PRINCES AVENUE, KINGSTON UPON HULL
        ]:
            return None

        if record.addressline6 in [
            "HU5 2RH",
            "HU5 3LT",
            "HU5 5NT",
        ]:
            return None

        return super().address_record_to_dict(record)
