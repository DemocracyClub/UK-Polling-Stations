from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MSS"
    addresses_name = (
        "2024-07-04/2024-05-31T14:22:13.337174/Democracy_Club__04July2024 (8).tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-31T14:22:13.337174/Democracy_Club__04July2024 (8).tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6.replace("\xa0", " ") in [
            # split
            "RH17 7DY",
            "BN6 9NA",
            "RH16 2QB",
            "RH19 4NQ",
            # suspect
            "RH10 4SH",
        ]:
            return None
        return super().address_record_to_dict(record)
