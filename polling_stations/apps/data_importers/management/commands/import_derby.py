from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DER"
    addresses_name = (
        "2022-05-05/2022-03-10T14:21:34.939559/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-10T14:21:34.939559/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030300432",  # FIRST FLOOR FLAT 28 CHAPEL STREET, SPONDON, DERBY
        ]:
            return None

        if record.addressline6 in [
            "DE23 6AR",
            "DE24 0LU",
            "DE21 4HF",
            "DE24 9HW",
            "DE21 4AW",
        ]:
            return None

        return super().address_record_to_dict(record)
