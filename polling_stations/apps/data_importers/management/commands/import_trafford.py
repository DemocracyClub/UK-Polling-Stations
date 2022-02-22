from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TRF"
    addresses_name = (
        "2022-05-05/2022-02-22T13:33:40.474278/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-22T13:33:40.474278/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070444818",  # FOUR OAKS CARE HOME, 28 WOOD LANE, PARTINGTON, MANCHESTER
            "100011682981",  # 2 BRIAR CLOSE, SALE, M33 5RG
        ]:
            return None

        if record.addressline6 in [
            "M33 2BT",
            "M41 6JU",
            "M41 9AS",
            "M32 0SF",
            "M16 9DA",
        ]:
            return None

        return super().address_record_to_dict(record)
