from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FAR"
    addresses_name = (
        "2022-05-05/2022-03-04T14:15:27.595084/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-04T14:15:27.595084/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.post_code in [
            "SO31 7BJ",
            "PO16 7LR",
            "PO14 4QS",
        ]:
            return None

        return rec
