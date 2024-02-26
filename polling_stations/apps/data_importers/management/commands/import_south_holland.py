from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHO"
    addresses_name = (
        "2024-05-02/2024-02-26T14:34:34.154424/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-26T14:34:34.154424/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030894500",  # BUSLEY, SOUTH DROVE, SPALDING
            "10094356949",  # LITTLE ACRE, SOUTH DROVE, SPALDING
            "100030888845",  # AMOW, MIDDLE MARSH ROAD, MOULTON MARSH, SPALDING
        ]:
            return None

        if record.addressline6 in [
            # split
            "PE12 9QJ",
            "PE6 0LR",
            # suspect
            "PE12 0HZ",
            "PE11 3GP",
            "PE12 8SG",
        ]:
            return None

        return super().address_record_to_dict(record)
