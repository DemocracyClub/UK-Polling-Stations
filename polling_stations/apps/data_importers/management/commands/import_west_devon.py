from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WDE"
    addresses_name = (
        "2023-05-04/2023-03-10T14:02:41.313172/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-10T14:02:41.313172/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013758398",  # MOWHAY BARN, HIGHER CARLEY BARNS, LIFTON
            "10013754124",  # OLD MILL, HOLDITCH FARM, MARY TAVY, TAVISTOCK
        ]:
            return None

        if record.addressline6 in [
            # split
            "EX20 1QB",
            "EX20 3NW",
            "EX20 1SY",
            "EX20 2TP",
            "EX20 2SD",
        ]:
            return None

        return super().address_record_to_dict(record)
