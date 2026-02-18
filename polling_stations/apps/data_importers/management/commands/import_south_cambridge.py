from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SCA"
    addresses_name = (
        "2026-05-07/2026-02-18T11:00:52.688916/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-18T11:00:52.688916/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    # Below warnings checked, no correction needed:
    # WARNING: Polling station Meadows Community Centre (8932) is in Cambridge City Council (CAB)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10095471389",  # FOXHILL SIDE, HINTON WAY, GREAT SHELFORD, CAMBRIDGE, CB22 5AN
                "10096204414",  # BEAUFORT, STATION ROAD, LONGSTANTON, CAMBRIDGE
                "10095469809",  # THE COPPICE CARAVAN, STATION ROAD, LONGSTANTON, CAMBRIDGE
                "10095469885",  # FLEDGLING BARN, BRIDGEFOOT, BARLEY ROAD, HEYDON, ROYSTON
                "10033031432",  # GREENGAGE COTTAGE, BURY LANE, MELBOURN, ROYSTON
                "10096204379",  # HIGH BARN, SHINGAY ROAD, STEEPLE MORDEN, ROYSTON
                "10003185702",  # CHAPELGATE, ST. NEOTS ROAD, DRY DRAYTON, CAMBRIDGE
                "10095471389",  # FOXHILL SIDE, HINTON WAY, GREAT SHELFORD, CAMBRIDGE
                "10096207221",  # REDCROFT LODGE, STATION ROAD, LONGSTANTON, CAMBRIDGE, CB24 3DS
                "10096207222",  # REDCROFT BARN, STATION ROAD, LONGSTANTON, CAMBRIDGE, CB24 3DS
                "10095469809",  # THE COPPICE CARAVAN, STATION ROAD, LONGSTANTON, CAMBRIDGE, CB24 3DS
                "10008079271",  # CROWDEAN, CROWDEAN LANE, ELSWORTH, CAMBRIDGE, CB23 4LA
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "SG8 0BD",
            "CB21 5LF",
        ]:
            return None

        return super().address_record_to_dict(record)
