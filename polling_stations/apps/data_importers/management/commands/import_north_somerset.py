from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NSM"
    addresses_name = (
        "2024-05-02/2024-03-21T10:16:21.138046/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-21T10:16:21.138046/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "24138946",  # FLAT AT STAR INN RHODYATE HILL, BRISTOL
            "24080907",  # MARLBRO, THE BATCH, BACKWELL, BRISTOL
            "24155623",  # 71 LYEFIELD ROAD, KEWSTOKE, WESTON-SUPER-MARE
            "24014702",  # 30A BYRON ROAD, LOCKING, WESTON-SUPER-MARE
            "24141074",  # 11A BYRON ROAD, WESTON-SUPER-MARE
            "24013232",  # 6 PURN LANE, WESTON-SUPER-MARE
            "24148079",  # TWIN ELM FARM HOUSE, STOCK LANE, CONGRESBURY, BRISTOL
            "24058834",  # BAY TREE COTTAGE, LANGFORD ROAD, LANGFORD, BRISTOL
            "24076278",  # ASHTON HILL HOUSE, WESTON ROAD, FAILAND, BRISTOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BS24 8GE",
            "BS20 0LJ",
            "BS22 6EA",
            "BS40 7AP",
            # suspect
            "BS49 4FJ",  # CLARENCE GROVE, CLAVERHAM, BRISTOL
            "BS23 1WN",
            "BS23 1FHJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St James Church Hall, 52 Woodborough Road, Winscombe, BS25 1BA
        # easting/northing is terribly wrong
        if record.polling_place_id == "18143":
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )

        # Wick St. Lawrence Village Hall, Wick St. Lawrence, BS22 7YP
        # Wick St Lawrence Village Hall, Wick St Lawrence, BS22 7YP
        # Those two stations addresses are almost identical (St vs St.),
        # but for some reason easting/northing is different
        if record.polling_place_id in ["18138", "18136"]:
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )

        return super().station_record_to_dict(record)
