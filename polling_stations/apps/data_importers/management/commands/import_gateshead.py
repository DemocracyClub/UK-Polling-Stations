from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GAT"
    addresses_name = (
        "2023-05-04/2023-03-14T11:30:54.886338/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-14T11:30:54.886338/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093489937",  # 1B SPLIT CROW ROAD, HIGH FELLING, GATESHEAD
            "100000029999",  # 125 ELLISON ROAD, GATESHEAD
        ]:
            return None

        if record.addressline6 in [
            # split
            "NE9 5XP",
            "NE9 6JR",
            # wrong
            "NE39 2EA",
            "NE17 7BQ",
        ]:
            return None

        return super().address_record_to_dict(record)
