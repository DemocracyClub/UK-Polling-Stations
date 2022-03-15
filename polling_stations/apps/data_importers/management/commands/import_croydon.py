from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRY"
    addresses_name = (
        "2022-05-05/2022-03-15T22:27:09.311565/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-15T22:27:09.311565/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100020676357",  # 18A CROHAM ROAD, SOUTH CROYDON
        ]:
            return None

        if record.addressline6 in [
            "CR0 0NX",
            "CR0 2JB",
            "CR0 4BF",
            "CR2 0JB",
            "CR5 2YS",
            "CR5 2FN",
        ]:
            return None

        return super().address_record_to_dict(record)
