from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SCA"
    addresses_name = "2024-07-04/2024-06-04T11:27:16.291188/SCA_combined.tsv"
    stations_name = "2024-07-04/2024-06-04T11:27:16.291188/SCA_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    # Below warnings checked, no correction needed:
    # WARNING: Polling station Meadows Community Centre (8932) is in Cambridge City Council (CAB)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10096204414",  # BEAUFORT, STATION ROAD, LONGSTANTON, CAMBRIDGE
            "10095469809",  # THE COPPICE CARAVAN, STATION ROAD, LONGSTANTON, CAMBRIDGE
            "10003191905",  # LITTLE BARHAM HALL, BARTLOW, CAMBRIDGE
            "10091625172",  # LITTLE BARHAM HALL, BARTLOW, CAMBRIDGE
            "10033028149",  # NEW BUNGALOW, CHRISHALL GRANGE, HEYDON, ROYSTON
            "10095469885",  # FLEDGLING BARN, BRIDGEFOOT, BARLEY ROAD, HEYDON, ROYSTON
            "10033031432",  # GREENGAGE COTTAGE, BURY LANE, MELBOURN, ROYSTON
            "10096204379",  # HIGH BARN, SHINGAY ROAD, STEEPLE MORDEN, ROYSTON
            "10008080007",  # OAKDENE, MONKFIELD, BOURN, CAMBRIDGE
            "10008079271",  # CROWDEAN, CROWDEAN LANE, ELSWORTH, CAMBRIDGE
            "10003194120",  # THE OAKS, SCHOOL LANE, LOWER CAMBOURNE, CAMBRIDGE
            "200002748859",  # TWO POTS COTTAGES ST NEOTS ROAD, BOURN
            "10003185702",  # CHAPELGATE, ST. NEOTS ROAD, DRY DRAYTON, CAMBRIDGE
            "10095471389",  # FOXHILL SIDE, HINTON WAY, GREAT SHELFORD, CAMBRIDGE
            "10003195362",  # RIVER COTTAGE, SAWSTON ROAD, STAPLEFORD, CAMBRIDGE
            "100091416223",  # LORDS BRIDGE STATIONHOUSE, WIMPOLE ROAD, BARTON, CAMBRIDGE
            "10033031425",  # MOUNT FARMHOUSE MOUNT FARM CHALKY LANE, BABRAHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CB21 5LF",
            "SG8 0BD",
            # looks wrong
            "SG7 6SD",
            "SG7 5RW",
        ]:
            return None

        return super().address_record_to_dict(record)
