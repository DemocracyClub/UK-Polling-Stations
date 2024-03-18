from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWL"
    addresses_name = (
        "2024-05-02/2024-03-18T16:40:04.016144/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-18T16:40:04.016144/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003503741",  # OLD FARMHOUSE, NOTTINGHAM ROAD, STAUNTON HAROLD, ASHBY-DE-LA-ZOUCH
            "10002361080",  # KEEPERS COTTAGE, KEGWORTH LANE, LONG WHATTON, LOUGHBOROUGH
            "200003505244",  # THE AVIARY, WARREN LANE, WHITWICK, COALVILLE
        ]:
            return None

        if record.addressline6 in [
            # split
            "DE74 2DE",
        ]:
            return None

        return super().address_record_to_dict(record)
