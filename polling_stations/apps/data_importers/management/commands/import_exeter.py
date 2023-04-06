from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EXE"
    addresses_name = (
        "2023-05-04/2023-04-06T16:06:54.372260/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-06T16:06:54.372260/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091473295",  # EXE VIEW LODGE STOKE HILL, EXETER
            "100040222032",  # ARGYLL GARDENS, LOWER ARGYLL ROAD, EXETER
            "10023116924",  # PARK HOUSE, PARK LANE, EXETER
            "10023121146",  # 210A TOPSHAM ROAD, EXETER
            "100040241841",  # BELLENDEN, WREFORDS LANE, EXETER
        ]:
            return None

        if record.addressline6 in [
            "EX2 7AY",
            "EX4 9HE",
            "EX2 7TF",
            "EX4 5AJ",
        ]:
            return None

        return super().address_record_to_dict(record)
