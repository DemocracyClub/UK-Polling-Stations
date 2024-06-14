from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EDE"
    addresses_name = "2024-07-04/2024-06-23T07:55:42.283062/ede-combined.tsv"
    stations_name = "2024-07-04/2024-06-23T07:55:42.283062/ede-combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094722867",  # MOLLYS COTTAGE SNODWELL FARM POST LANE, COTLEIGH
        ]:
            return None

        if record.addressline6.replace("\xa0", " ") in [
            # split
            "EX14 4SE",
            "EX5 1LN",
        ]:
            return None

        return super().address_record_to_dict(record)
