from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EXE"
    addresses_name = (
        "2022-05-05/2022-03-14T16:19:01.344084/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-14T16:19:01.344084/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091473295",  # EXE VIEW LODGE STOKE HILL, EXETER
        ]:
            return None

        if record.addressline6 in [
            "EX2 7AY",
            "EX4 9HE",
            "EX2 7TF",
            "EX4 5AJ",
        ]:
            return None

        return super().address_record_to_dict(record)
