from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MSS"
    addresses_name = (
        "2024-05-02/2024-03-21T11:19:04.829570/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-21T11:19:04.829570/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6.replace("\xa0", " ") in [
            # split
            "RH17 7DY",
            "BN6 9NA",
            "RH16 2QB",
            # suspect
            "RH10 4SH",
        ]:
            return None
        return super().address_record_to_dict(record)
