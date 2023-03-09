from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAW"
    addresses_name = (
        "2023-05-04/2023-03-09T10:20:20.081832/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T10:20:20.081832/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "10093004484",  # FLAT THE DOVECOTE HILL TOP, WEST BROMWICH B70 0SD
            "10094430909",  # 586B BEARWOOD ROAD, SMETHWICK
        ]:
            return None

        if record.addressline6 in [
            "B69 4BZ",
            "B71 2LS",
            # split
            "B67 7EP",
            "B65 0BS",
            "DY4 7TY",
            "DY4 9NB",
        ]:
            return None

        return super().address_record_to_dict(record)
