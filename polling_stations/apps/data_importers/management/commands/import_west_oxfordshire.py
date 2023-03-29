from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOX"
    addresses_name = (
        "2023-05-04/2023-03-17T16:48:51.040027/Democracy_Club__04May2023 230317.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-17T16:48:51.040027/Democracy_Club__04May2023 230317.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "OX28 6DH",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
