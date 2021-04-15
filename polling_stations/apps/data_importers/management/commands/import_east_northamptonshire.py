from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ENO"
    addresses_name = (
        "2021-03-26T11:17:25.639067/Democracy_Club__06May2021-2nd run 25 3 2021.tsv"
    )
    stations_name = (
        "2021-03-26T11:17:25.639067/Democracy_Club__06May2021-2nd run 25 3 2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093005561"  # MOONBEAM WOODFORD RIVERSIDE MARINA ADDINGTON ROAD, WOODFORD
        ]:
            return None

        if record.addressline6 in [
            "NN9 5UF",
            "NN14 3BY",
            "NN10 9JD",
            "NN10 9NJ",
            "NN14 3HB",
            "PE8 5BA",
            "NN10 6EU",
            "NN10 0NZ",
        ]:
            return None

        return super().address_record_to_dict(record)
