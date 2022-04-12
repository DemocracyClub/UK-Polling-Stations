from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HYN"
    addresses_name = (
        "2022-05-05/2022-04-12T10:49:34.302894/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-12T10:49:34.302894/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070894060",
            "10009967792",
        ]:
            return None

        if record.addressline6 in [
            "BB5 5QA",  # split
            "BB5 6PW",  # funny districting
        ]:
            return None

        return super().address_record_to_dict(record)
