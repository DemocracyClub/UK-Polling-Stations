from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWL"
    addresses_name = (
        "2024-07-04/2024-05-30T11:05:57.723777/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-30T11:05:57.723777/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003503741",  # OLD FARMHOUSE, NOTTINGHAM ROAD, STAUNTON HAROLD, ASHBY-DE-LA-ZOUCH
            "10002361080",  # KEEPERS COTTAGE, KEGWORTH LANE, LONG WHATTON, LOUGHBOROUGH
            "200003505244",  # THE AVIARY, WARREN LANE, WHITWICK, COALVILLE
            "10002353672",  # THE MALTINGS, STATION ROAD, HUGGLESCOTE, COALVILLE
            "10002361801",  # FLAT 1, SHELLBROOK HOUSE IC, MARKET STREET, ASHBY-DE-LA-ZOUCH
            "100030551333",  # 68 BURTON ROAD, ASHBY-DE-LA-ZOUCH
            "10002345003",  # AMBROW HILL, ISLEY WALTON, CASTLE DONINGTON, DERBY
        ]:
            return None

        if record.addressline6 in [
            # split
            "DE74 2DE",
        ]:
            return None

        return super().address_record_to_dict(record)
