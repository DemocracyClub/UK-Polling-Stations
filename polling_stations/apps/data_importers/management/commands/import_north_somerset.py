from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NSM"
    addresses_name = (
        "2023-05-04/2023-04-19T13:44:55.694586/Democracy_Club__04May2023 (2).tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-19T13:44:55.694586/Democracy_Club__04May2023 (2).tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "24138946",  # FLAT AT STAR INN RHODYATE HILL, BRISTOL
            "24080907",  # MARLBRO, THE BATCH, BACKWELL, BRISTOL
            "24155623",  # 71 LYEFIELD ROAD, KEWSTOKE, WESTON-SUPER-MARE
            "24147349",  # 20A QUEENS ROAD, WESTON-SUPER-MARE
            "24014702",  # 30A BYRON ROAD, LOCKING, WESTON-SUPER-MARE
            "24141074",  # 11A BYRON ROAD, WESTON-SUPER-MARE
            "24013232",  # 6 PURN LANE, WESTON-SUPER-MARE24148079
            "24148079",  # TWIN ELM FARM HOUSE, STOCK LANE, CONGRESBURY, BRISTOL
            "24058834",  # BAY TREE COTTAGE, LANGFORD ROAD, LANGFORD, BRISTOL
            "24076278",  # ASHTON HILL HOUSE, WESTON ROAD, FAILAND, BRISTOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BS22 6EA",
            "BS20 0LJ",
            "BS40 7AP",
            "BS49 4FJ",  # CLARENCE GROVE, CLAVERHAM, BRISTOL
            "BS24 7NS",  # BALL AVENUE, LOCKING, WESTON-SUPER-MARE
            "BS24 7PB",  # ROBINSON PLACE, LOCKING, WESTON-SUPER-MARE
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St James Church Hall, 52 Woodborough Road, Winscombe, BS25 1BA
        # easting/northing is terribly wrong
        if record.polling_place_id == "13127":
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )

        # Wick St. Lawrence Village Hall, Wick St. Lawrence, BS22 7YP
        # Wick St Lawrence Village Hall, Wick St Lawrence, BS22 7YP
        # Those two stations addresses are almost identical (St vs St.),
        # but for some reason easting/northing is different
        if record.polling_place_id in ["13317", "13313"]:
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )

        return super().station_record_to_dict(record)
