from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NSM"
    addresses_name = "2024-07-04/2024-06-25T10:54:21.480098/NSM_combined.csv"
    stations_name = "2024-07-04/2024-06-25T10:54:21.480098/NSM_combined.csv"
    elections = ["2024-07-04"]

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
            "BS22 6EA",
            "BS40 7AP",
            "BS20 0LJ",
            # suspect
            "BS23 1WN",
            "BS23 1FH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St James Church Hall, 52 Woodborough Road, Winscombe, BS25 1BA
        # easting/northing is terribly wrong
        if record.polling_place_id == "19201":
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )

        return super().station_record_to_dict(record)
