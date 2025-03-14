from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SCA"
    addresses_name = (
        "2025-05-01/2025-03-14T09:31:36.010664/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-14T09:31:36.010664/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    # Below warnings checked, no correction needed:
    # WARNING: Polling station Meadows Community Centre (8932) is in Cambridge City Council (CAB)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10096204414",  # BEAUFORT, STATION ROAD, LONGSTANTON, CAMBRIDGE
            "10095469809",  # THE COPPICE CARAVAN, STATION ROAD, LONGSTANTON, CAMBRIDGE
            "10095469885",  # FLEDGLING BARN, BRIDGEFOOT, BARLEY ROAD, HEYDON, ROYSTON
            "10033031432",  # GREENGAGE COTTAGE, BURY LANE, MELBOURN, ROYSTON
            "10096204379",  # HIGH BARN, SHINGAY ROAD, STEEPLE MORDEN, ROYSTON
            "10003185702",  # CHAPELGATE, ST. NEOTS ROAD, DRY DRAYTON, CAMBRIDGE
            "10095471389",  # FOXHILL SIDE, HINTON WAY, GREAT SHELFORD, CAMBRIDGE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SG8 0BD",
            "CB21 5LF",
        ]:
            return None

        return super().address_record_to_dict(record)
