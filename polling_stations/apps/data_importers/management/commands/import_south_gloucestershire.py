from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SGC"
    addresses_name = "2024-07-04/2024-05-29T08:37:58.830058/Democracy_Club__04July2024 FABS & TANDY.tsv"
    stations_name = "2024-07-04/2024-05-29T08:37:58.830058/Democracy_Club__04July2024 FABS & TANDY.tsv"
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
            "BS37 6DF",
            "BS37 7BZ",
            "BS32 4AH",
        ]:
            return None
        return super().address_record_to_dict(record)
