from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWL"
    addresses_name = (
        "2023-05-04/2023-05-02T18:33:00.761150/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-05-02T18:33:00.761150/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003503741",  # OLD FARMHOUSE, NOTTINGHAM ROAD, STAUNTON HAROLD, ASHBY-DE-LA-ZOUCH        ]:
        ]:
            return None

        if record.addressline6 in [
            # split
            "DE74 2DE",
        ]:
            return None

        return super().address_record_to_dict(record)
