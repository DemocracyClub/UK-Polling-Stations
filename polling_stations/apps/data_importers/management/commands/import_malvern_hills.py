from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAV"
    addresses_name = (
        "2023-05-04/2023-02-07T10:13:27.529328/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-02-07T10:13:27.529328/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # St Mary`s Church Hall Sherrards Green Road Malvern
        if record.polling_place_id == "13513":
            record = record._replace(
                polling_place_easting="379264", polling_place_northing="246303"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093062320",  # LOG CABIN AT 2 STRAWBERRY COTTAGE A443 NEWNHAM BRIDGE, NEWNHAM BRIDGE
            "10014087730",  # 1 STRAWBERRY COTTAGE, NEWNHAM BRIDGE, TENBURY WELLS
            "10014087731",  # 2 STRAWBERRY COTTAGE, NEWNHAM BRIDGE, TENBURY WELLS
            "10014087728",  # KEEPERS COTTAGE, NEWNHAM BRIDGE, TENBURY WELLS
            "10014088277",  # 2 BRICKYARD COTTAGES, FEATHERBED LANE, NEWNHAM BRIDGE, TENBURY WELLS"
            "10014088278",  # 1 BRICKYARD COTTAGES, FEATHERBED LANE, NEWNHAM BRIDGE, TENBURY WELLS
            "10014090439",  # BAKERS COTTAGE, WICHENFORD, WORCESTER
            "10024321016",  # THE CARTHOUSE, BIRCHLEY MILL, BOCKLETON ROAD, OLDWOOD, TENBURY WELLS
            "100120595356",  # HUNTERS LODGE, MAIN ROAD, KEMPSEY, WORCESTER
            "100121268209",  # CHERRY TREE COTTAGE MOSELEY ROAD, HALLOW
            "10014090474",  # PENTOWAN, WICHENFORD, WORCESTER
        ]:
            return None

        if record.addressline6 in [
            "WR1 42WE",
            "WR2 4TD",
            "WR14 4JY",
            "WR2 6RB",
            "WR6 6BH",
            "WR15 8DP",
            "WR8 0AN",
        ]:
            return None

        return super().address_record_to_dict(record)
