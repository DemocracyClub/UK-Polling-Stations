from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "VAL"
    addresses_name = "2023-05-04/2023-03-13T14:59:04.963906/Vale of White Horse - Democracy_Club__04May2023.TSV"
    stations_name = "2023-05-04/2023-03-13T14:59:04.963906/Vale of White Horse - Democracy_Club__04May2023.TSV"
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "SN7 8DJ",
            "OX13 5GW",
            "OX13 5ND",
            # look wrong
            "SN7 7BQ",
        ]:
            return None

        return super().address_record_to_dict(record)
