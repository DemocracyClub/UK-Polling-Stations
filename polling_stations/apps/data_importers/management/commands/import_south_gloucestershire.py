from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SGC"
    addresses_name = (
        "2024-05-02/2024-03-20T11:58:57.790251/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-20T11:58:57.790251/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
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
            "BS15 3HW",
            "BS32 4AH",
            "BS16 4LZ",
            "BS15 3HP",
            "BS37 7BZ",
            "BS37 6DF",
            "BS30 5TP",
        ]:
            return None
        return super().address_record_to_dict(record)
