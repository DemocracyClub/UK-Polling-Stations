from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SGC"
    addresses_name = "2024-07-04/2024-06-24T14:59:47.769765/SGC_combined.tsv"
    stations_name = "2024-07-04/2024-06-24T14:59:47.769765/SGC_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "689538",  # THE ANNEXE HAM FARM COTTAGE EMERSONS GREEN LANE, EMERSONS GREEN
            "546172",  # HAM FARM COTTAGE, EMERSONS GREEN LANE, EMERSONS GREEN, BRISTOL
            "690417",  # LOVELL PLACE, SPARROWBILL WAY, PATCHWAY, BRISTOL
        ]:
            return None
        if record.addressline6 in [
            # split
            "BS30 5TP",
            "BS37 7BZ",
            "BS37 6DF",
            "BS15 3HW",
            "BS16 4LZ",
            "BS15 3HP",
            "BS32 4AH",
        ]:
            return None
        return super().address_record_to_dict(record)
