from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAL"
    addresses_name = "2024-07-04/2024-06-13T16:01:20.257096/MAL_combined.tsv"
    stations_name = "2024-07-04/2024-06-13T16:01:20.257096/MAL_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094633716",  # PARK HOUSE MALDON ROAD, LATCHINGDON
        ]:
            return None

        if record.addressline6.strip() in [
            # split
            "CM9 6YN",
            "CM9 4NY",
            # suspect
            "CM9 4RA",
        ]:
            return None

        return super().address_record_to_dict(record)
