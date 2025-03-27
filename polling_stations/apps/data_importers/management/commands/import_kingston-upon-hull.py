from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KHL"
    addresses_name = "2025-05-01/2025-03-27T11:43:28.234897/Democracy Club.tsv"
    stations_name = "2025-05-01/2025-03-27T11:43:28.234897/Democracy Club.tsv"
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "21133711",  # FLAT OVER 19 18-19 WITHAM, KINGSTON UPON HULL
            "21133712",  # FLAT OVER 121 121-127 WITHAM, KINGSTON UPON HULL
        ]:
            return None

        if record.addressline6 in [
            # split
            "HU5 5NT",
            "HU5 3LT",
            "HU5 2RH",
        ]:
            return None

        return super().address_record_to_dict(record)
