from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PRE"
    addresses_name = (
        "2026-05-07/2026-03-18T17:08:38.362206/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-18T17:08:38.362206/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007606520",  # WILLOW BANK, INGLEWHITE ROAD, GOOSNARGH, PRESTON
            "100010579401",  # 16A WOODPLUMPTON ROAD, ASHTON-ON-RIBBLE, PRESTON
            "100010574023",  # 219 TULKETH BROW, ASHTON-ON-RIBBLE, PRESTON
            "100012402901",  # MEADOWBROOK, INGLEWHITE ROAD, GOOSNARGH, PRESTON
            "100012401519",  # INGLENOOK BARN, CARRON LANE, INGLEWHITE, PRESTON
            "100012405502",  # 105A WHITTINGHAM LANE, BROUGHTON, PRESTON
            "10013339494",  # SIMPSON HOUSE, FERNYHALGH LANE, FULWOOD, PRESTON
            "100010534827",  # BARBER SHOP, 109A BLACK BULL LANE, FULWOOD, PRESTON
            "10093760272",  # 17 BLYTHE ROAD, LIGHTFOOT GREEN, PRESTON
            "100012746089",  # 119 OXFORD STREET, PRESTON
            "10093760392",  # 48 CHELTENHAM CRESCENT, LIGHTFOOT GREEN, PRESTON
            "10002219398",  # STONE COTTAGE, FISHWICK BOTTOMS, PRESTON
        ]:
            return None

        if record.addressline6 in [
            # split
            "PR4 0YX",
            # looks wrong
            "PR1 3SG",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # WARNING: Polling station Longridge Town Football Club is in Ribble Valley Borough Council (RIB)
        # small location correction for: Longridge Town Football Club, Inglewhite Road, Longridge, Preston, PR3 2NA
        if record.polling_place_id == "5726":
            record = record._replace(
                polling_place_easting="359906", polling_place_northing="438020"
            )

        # location correction for: Millennium Hall, Neapsands Close, Fulwood, Preston, PR2 9AQ
        if record.polling_place_id == "5662":
            record = record._replace(
                polling_place_easting="355831", polling_place_northing="432404"
            )

        return super().station_record_to_dict(record)
