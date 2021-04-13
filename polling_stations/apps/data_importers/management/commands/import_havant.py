from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAA"
    addresses_name = "2021-03-25T12:55:41.884654/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-25T12:55:41.884654/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062456253",  # 37 LONDON ROAD, COWPLAIN, WATERLOOVILLE
        ]:
            return None

        if record.addressline6 in [
            "PO9 2DT",
            "PO9 3EZ",
            "PO8 8BB",
            "PO10 7NH",
            "PO10 7HN",
            "PO8 9UB",
        ]:
            return None

        return super().address_record_to_dict(record)
