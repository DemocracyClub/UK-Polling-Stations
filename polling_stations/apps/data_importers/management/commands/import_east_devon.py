from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EDE"
    addresses_name = (
        "2024-05-02/2024-03-21T10:21:06.232080/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-21T10:21:06.232080/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094722867",  # MOLLYS COTTAGE SNODWELL FARM POST LANE, COTLEIGH
        ]:
            return None

        if record.addressline6.replace("\xa0", " ") in [
            # split
            "EX14 4SE",
            "EX5 1LN",
        ]:
            return None

        return super().address_record_to_dict(record)
