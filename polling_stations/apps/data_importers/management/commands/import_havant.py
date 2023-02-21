from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAA"
    addresses_name = (
        "2022-05-05/2022-03-10T13:42:05.933404/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-10T13:42:05.933404/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "PO9 2DT",
            "PO8 8BB",
            "PO10 7NH",
            "PO8 9UB",
            "PO11 9LA",
        ]:
            return None

        return super().address_record_to_dict(record)
