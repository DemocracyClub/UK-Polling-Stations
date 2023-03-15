from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ASF"
    addresses_name = (
        "2023-05-04/2023-03-15T10:12:47.076239/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-15T10:12:47.076239/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004389187",  # MOBILE HOME AT CLOVER FARM THE PINNOCK, PLUCKLEY
        ]:
            return None

        if record.addressline6 in ["TN24 9FA", "TN25 7AS"]:
            return None

        return super().address_record_to_dict(record)
