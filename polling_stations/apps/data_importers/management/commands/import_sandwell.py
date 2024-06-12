from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAW"
    addresses_name = (
        "2024-07-04/2024-06-12T17:22:21.833014/Democracy_Club__04July2024 (27).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-12T17:22:21.833014/Democracy_Club__04July2024 (27).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "10093004484",  # FLAT THE DOVECOTE HILL TOP, WEST BROMWICH B70 0SD
            "10094430909",  # 586B BEARWOOD ROAD, SMETHWICK
        ]:
            return None

        if record.addressline6 in [
            # split
            "DY4 7TY",
            "B65 0BS",
            "DY4 9NB",
            "B67 7EP",
            # suspect
            "B69 4BZ",
            "B71 2LS",
        ]:
            return None

        return super().address_record_to_dict(record)
